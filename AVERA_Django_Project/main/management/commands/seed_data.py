from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import *

class Command(BaseCommand):
    help = "Create demo data for AVERA"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("Admin@12345")
            admin_user.email = "admin@avera.local"
            admin_user.user_type = "admin"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        admin_profile, _ = Admin.objects.get_or_create(user=admin_user, defaults={"name":"AVERA Admin","email":"admin@avera.local"})

        org, _ = CareOrganization.objects.get_or_create(
            organization_id="ORG-001",
            defaults={
                "organization_name":"Hope Children Care",
                "address":"Dhaka, Bangladesh",
                "phone":"+880 1XXXXXXXXX",
                "email":"hope@example.com",
                "description":"A demo verified care organization for the academic project.",
                "verification_status":"verified"
            }
        )
        if not AdoptionInformation.objects.exists():
            AdoptionInformation.objects.create(
                title="Understanding Child Adoption",
                description="A clear overview of adoption awareness, preparation and responsible decision-making.",
                eligibility="Eligibility depends on the applicable law and authority. This academic website provides information only.",
                required_documents="Identity documents, financial information and other documents may be requested by the relevant authority.",
                adoption_process="Learn → Check official requirements → Contact the appropriate authority or organization → Follow the official process.",
                contact_information="Always verify current requirements with the relevant authority."
            )
        if not AwarenessContent.objects.exists():
            AwarenessContent.objects.create(
                title="Adoption: Information Before Inspiration",
                description="Responsible adoption starts with accurate information, realistic expectations and respect for children.",
                content_type="guide",
                created_by=admin_profile
            )
            AwarenessContent.objects.create(
                title="Myth & Fact: Adoption",
                description="Read reliable information and avoid assumptions about adoption eligibility and process.",
                content_type="myth",
                created_by=admin_profile
            )
        if not FAQ.objects.exists():
            FAQ.objects.create(faq_id="FAQ-001", question="Does AVERA process legal adoption?", answer="No. AVERA is an informational and awareness platform. Users should contact the relevant official authority for legal procedures.", category="General")
            FAQ.objects.create(faq_id="FAQ-002", question="Can I support children without adopting?", answer="Yes. The platform provides gift-support and wishlist features for meaningful non-adoption support.", category="Support")
        if not Wishlist.objects.exists():
            Wishlist.objects.create(
                wishlist_id="WL-DEMO01", organization=org, title="School Supplies",
                description="Basic educational supplies for children.",
                item_name="Notebooks", quantity_needed=50, quantity_received=12,
                priority="High", status="Partially fulfilled"
            )
        self.stdout.write(self.style.SUCCESS("Demo data ready. Admin login: admin / Admin@12345"))
