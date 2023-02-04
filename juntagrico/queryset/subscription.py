import datetime

from django.db import connection
from django.db.models import When, Q, F, ExpressionWrapper, DurationField, Case, DateField, FloatField, Sum, Subquery, OuterRef
from django.db.models.functions import Least, Greatest, Round, Cast, Coalesce, ExtractDay
from django.utils.decorators import method_decorator
from polymorphic.query import PolymorphicQuerySet

from juntagrico.entity.member import SubscriptionMembership
from juntagrico.util.temporal import default_to_business_year


def assignments_in_subscription_membership(start, end, **extra_filters):
    """
    Based on example in documentation
    https://docs.djangoproject.com/en/4.1/ref/models/expressions/#using-aggregates-within-a-subquery-expression
    :param start: beginning of period of interest
    :param end: end of period of interest
    :param extra_filters: additional filters to apply on SubscriptionMembership selection
    :return: a queryset returning the sub of the assignments amounts, ready for use in a subquery of a subscription
    """
    return SubscriptionMembership.objects.filter(subscription=OuterRef('pk')).filter(
        Q(leave_date__isnull=True) |
        Q(leave_date__gte=F('member__assignment__job__time__date')),
        join_date__lte=F('member__assignment__job__time__date'),
        member__assignment__job__time__date__gte=start,
        member__assignment__job__time__date__lte=end,
        **extra_filters
    ).order_by().values('subscription').annotate(
        total=Sum('member__assignment__amount', default=0.0),
    ).values('total')


class SubscriptionQuerySet(PolymorphicQuerySet):
    microseconds_in_day = 24 * 3600 * 10 ** 6
    days_in_year = 365  # ignore leap years
    one_day = datetime.timedelta(1)

    @method_decorator(default_to_business_year)
    def annotate_assignment_counts(self, start=None, end=None, of_member=None, prefix=''):
        """
        count assignments of the subscription members for the jobs they did within their subscription membership and in the period of interest.
        :param start: beginning of period of interest, default: start of current business year.
        :param end: end of period of interest, default: end of current business year.
        :param of_member: if set, assignments of the given member are also counted and stored in `member_assignment_count` and `member_core_assignment_count`.
        :param prefix: prefix for the resulting attribute names, default=''.
        :return: the queryset of subscriptions with annotations `assignment_count` and `core_assignment_count`.
        """
        # Using subquery as otherwise the sum would be wrong when used in combination with the annotations of annotate_required_assignments
        qs = self
        if of_member:
            qs = qs.annotate(**{
                prefix + 'member_assignment_count': Coalesce(Subquery(assignments_in_subscription_membership(start, end, member=of_member)), 0.0),
                prefix + 'member_core_assignment_count': Coalesce(Subquery(assignments_in_subscription_membership(
                    start, end,
                    member=of_member,
                    member__assignment__core_cache=True
                )), 0.0)
            })
        return qs.annotate(**{
            prefix + 'assignment_count': Coalesce(Subquery(assignments_in_subscription_membership(start, end)), 0.0),
            prefix + 'core_assignment_count': Coalesce(Subquery(assignments_in_subscription_membership(start, end, member__assignment__core_cache=True)), 0.0),
        })

    @method_decorator(default_to_business_year)
    def annotate_required_assignments(self, start=None, end=None):
        """
        calculate the required number of (core) assignments of the subscription given the parts in it, discounted with their duration within the period of interest.
        :param start: beginning of period of interest, default: start of current business year.
        :param end: end of period of interest, default: end of current business year.
        :return: the queryset of subscriptions with annotations `required_assignments` and `required_core_assignments`.
        """
        return self.alias(
            # convert trial days into duration. Minus 1 to end up at the end of the last trial day, e.g., 1. + 30 days = 30. (not 31.)
            parts__type__trial_duration=ExpressionWrapper(F('parts__type__trial_days') * self.one_day, DurationField()) - self.one_day,
            # find (assumed) deactivation date of part
            parts__forecast_final_date=Least(
                end,  # limit final date to period of interest
                Case(
                    # use deactivation date if set
                    When(parts__deactivation_date__isnull=False,
                         then='parts__deactivation_date'),
                    # on trial subs without deactivation date assume they will last for trial duration.
                    When(parts__type__trial_days__gt=0,
                         then=Cast(F('parts__activation_date') + F('parts__type__trial_duration'), DateField())),
                    # otherwise default to end of period
                    default=end,
                    output_field=DateField()
                )
            ),
            # number of days subscription part is actually active within period of interest. Add a day because activation day should also count to duration
            parts__duration_in_period=F('parts__forecast_final_date') - Greatest('parts__activation_date', start) + self.one_day,
            parts__duration_in_period_float=Greatest(
                0.0,  # ignore values <0 resulting from parts outside the period of interest
                # Tested on postgres (ExtractDay) and SQLite (Cast)
                ExtractDay('parts__duration_in_period')
                if connection.features.has_native_duration_field else
                Cast('parts__duration_in_period', FloatField()) / self.microseconds_in_day,
                output_field=FloatField()
            ),
            # number of days within which the assignments are required
            parts__reference_duration=Case(
                When(parts__type__trial_days__gt=0,
                     then='parts__type__trial_days'),
                default=self.days_in_year,
                output_field=FloatField()
            ),
            parts__required_assignments_discount=Case(
                # ignore parts that have not startet yet
                When(parts__activation_date__isnull=True,
                     then=0.0),
                # get discount ratio for required assignments
                default=F('parts__duration_in_period_float') / F('parts__reference_duration')
            )
        ).annotate(  # annotate the final results
            required_assignments=Round(Sum(F('parts__type__required_assignments') * F('parts__required_assignments_discount'), default=0.0)),
            required_core_assignments=Round(Sum(F('parts__type__required_core_assignments') * F('parts__required_assignments_discount'), default=0.0)),
        )

    def annotate_assignments_progress(self, prefix=''):
        """
        Calculate progress, i.e. percentage of done vs. required assignments
        can only be applied in combination with `annotate_required_assignments` and `annotate_assignment_counts`
        :param prefix: prefix to be used on the `assignment_count` and `core_assignment_count`. Use it to match the prefix applied with `annotate_assignment_counts`. default=''
        :return: the queryset of subscriptions with annotations `assignments_progress` and `core_assignments_progress`
        """
        return self.annotate(**{
            prefix + 'assignments_progress': Case(
                When(required_assignments=0,
                     then=100),
                default=F(prefix + 'assignment_count') / F('required_assignments') * 100,
                output_field=FloatField()
            ),
            prefix + 'core_assignments_progress': Case(
                When(required_core_assignments=0,
                     then=100),
                default=F(prefix + 'core_assignment_count') / F('required_core_assignments') * 100,
                output_field=FloatField()
            )
        })

    @method_decorator(default_to_business_year)
    def annotate_assignments(self, start=None, end=None, of_member=None, count_jobs_until=None):
        """
        annotate required and made assignments and calculated progress for core and in general
        count_jobs_until: only account for jobs until this date.
        :param start: beginning of period of interest, default: start of current business year.
        :param end: end of period of interest, default: end of current business year.
        :param of_member: if set, assignments of the given member are also counted and stored in `member_assignment_count` and `member_core_assignment_count`.
        :param count_jobs_until: if set, `annotate_assignment_counts` will only count until this date instead of end.
        :return: the queryset of subscriptions with annotations `assignment_count`, `core_assignment_count`, `required_assignments`, `required_core_assignments`,
        `assignments_progress` and `core_assignments_progress`.
        """
        return self.annotate_assignment_counts(start, count_jobs_until or end, of_member).\
            annotate_required_assignments(start, end).annotate_assignments_progress()