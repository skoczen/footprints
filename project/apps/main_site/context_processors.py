def intercom_custom_data(request):
    try:
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            return {
                "intercom_user_id": profile.pk,
                "intercom_name": profile.name,
                "intercom_premium_user": profile.premium_user,
                "intercom_num_drafts": profile.post_set.filter(is_draft=True).count(),
                "intercom_num_published_posts": profile.post_set.filter(is_draft=False).count(),
                "intercom_num_revisions": profile.postrevision_set.filter().count(),
                "intercom_num_reads": profile.read_set.count(),
                "intercom_num_fantastics": profile.fantastic_set.count(),
                "intercom_widget": {
                    "activator": "#Intercom"
                },
            }
    except:
        pass

    return {}

