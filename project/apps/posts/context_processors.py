def intercom_custom_data(request):
    try:
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            return {
                "intercom_user_id": profile.pk,
                "intercom_name": profile.name,
                # "intercom_premium_user": profile.premium_user,
                "intercom_widget": {
                    "activator": "#Intercom"
                },
            }
    except:
        pass

    return {}
