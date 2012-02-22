from django.shortcuts import get_object_or_404
import jingo

from django.contrib.auth.models import User
from challenges.models import Submission, Category
from projects.models import Project


def splash(request, project, slug, template_name='challenges/show.html'):
    """Show an individual project challenge."""
    project = get_object_or_404(Project, slug=project)
    challenge = get_object_or_404(project.challenge_set, slug=slug)
    entries = (Submission.objects.visible()
                                 .filter(phase__challenge=challenge)
                                 .order_by("?"))
    
    return jingo.render(request, 'ignite/splash.html', {
        'challenge': challenge,
        'project': project,
        'phases': list(enumerate(challenge.phases.all(), start=1)),
        'entries': entries[:10],
        'categories': Category.objects.get_active_categories(),
    })

def judges(request, project, slug, template_name='challenges/all_judges.html'):
    """ List all judges we have in the system """
    profiles = []
    for judge in User.objects.filter(groups__name='Judges'):
        profiles.append(judge.get_profile())

    return jingo.render(request, 'ignite/judges.html', {
        'profiles': profiles
    })
