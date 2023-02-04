from django import template
from django.utils import timezone

from juntagrico.dao.jobdao import JobDao

register = template.Library()


@register.simple_tag
def next_jobs(request):
    return JobDao.upcomming_jobs_for_member(request.user.member)


@register.simple_tag
def assignment_data(request):
    member = request.user.member
    if member.subscription_current is None:
        return None

    # calculate assignments
    sub = member.subscription_current.get_with_assignments(of_member=member, count_jobs_until=timezone.now().date())
    sub.remaining_assignments = max(
        sub.required_assignments - sub.assignment_count,
        sub.required_core_assignments - sub.core_assignment_count,
        0  # negative values would hide additionally made assignments
    )

    # for displaying
    return {
        'member_core': int(sub.member_core_assignment_count),
        'member': int(sub.member_assignment_count),
        'partner_core': int(sub.core_assignment_count - sub.member_core_assignment_count),
        'partner': int(sub.assignment_count - sub.member_assignment_count),
        'partner_core_bound': int(sub.member_assignment_count + sub.core_assignment_count - sub.member_core_assignment_count),
        'partner_bound': int(sub.assignment_count),
        'total': list(range(int(sub.assignment_count + sub.remaining_assignments))),
    }
