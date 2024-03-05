from api.models import Agency


def uni_validation(request):
    requested_url = request.build_absolute_uri()
    domain = requested_url.split("//")[1].split(".")[0]
    agency = Agency.objects.filter(agency_code=domain).exists()
    if agency:
        return True
    return False