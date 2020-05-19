from wagtail.contrib.redirects.models import Redirect
from wagtail.core import hooks


@hooks.register('after_move_page')
def after_move_page_hook(request, instance):
    old_path = Redirect.normalise_path(instance.url)
    instance.refresh_from_db()

    if supports_automatic_redirect(instance) and instance.live:
        Redirect.objects.update_or_create(
            old_path=old_path,
            defaults={
                'redirect_page': instance,
            }
        )

    create_redirect_objects_for_children(old_path, instance)


def supports_automatic_redirect(page):
    no_automatic_redirect = getattr(page, 'no_automatic_redirect', False)
    return not no_automatic_redirect


def create_redirect_objects_for_children(parent_old_slug, parent):
    if not parent.get_children():
        return
    else:
        for child_page in parent.get_children().specific():
            old_path = Redirect.normalise_path(
                parent_old_slug + '/' + child_page.slug)

            if supports_automatic_redirect(child_page) and child_page.live:
                Redirect.objects.update_or_create(
                    old_path=old_path,
                    defaults={
                        'redirect_page': child_page
                    }
                )

            create_redirect_objects_for_children(old_path, child_page)
