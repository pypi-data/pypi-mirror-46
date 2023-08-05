from django.urls.conf import path

from .patterns import subject_identifier, screening_identifier
from .views import (
    AeHomeView,
    AeListboardView,
    DeathReportListboardView,
    SubjectListboardView,
    SubjectDashboardView,
    ScreeningListboardView,
    NewTmgAeListboardView,
    OpenTmgAeListboardView,
    ClosedTmgAeListboardView,
    TmgDeathListboardView,
    TmgHomeView,
    TmgSummaryListboardView,
    SubjectReviewListboardView,
)

app_name = "ambition_dashboard"

urlpatterns = [
    path("tmg/", TmgHomeView.as_view(), name="tmg_home_url"),
    path("ae/", AeHomeView.as_view(), name="ae_home_url"),
]

urlpatterns += SubjectListboardView.urls(
    namespace=app_name, label="subject_listboard", identifier_pattern=subject_identifier
)
urlpatterns += ScreeningListboardView.urls(
    namespace=app_name,
    label="screening_listboard",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
urlpatterns += SubjectDashboardView.urls(
    namespace=app_name, label="subject_dashboard", identifier_pattern=subject_identifier
)


# urlpatterns += TmgAeListboardView.urls(
#     namespace=app_name, label="tmg_ae_listboard", identifier_pattern=subject_identifier
# )
urlpatterns += NewTmgAeListboardView.urls(
    namespace=app_name, label="new_tmg_ae_listboard", identifier_pattern=subject_identifier
)
urlpatterns += OpenTmgAeListboardView.urls(
    namespace=app_name, label="open_tmg_ae_listboard", identifier_pattern=subject_identifier
)
urlpatterns += ClosedTmgAeListboardView.urls(
    namespace=app_name, label="closed_tmg_ae_listboard", identifier_pattern=subject_identifier
)


urlpatterns += TmgDeathListboardView.urls(
    namespace=app_name,
    label="tmg_death_listboard",
    identifier_pattern=subject_identifier,
)
urlpatterns += TmgSummaryListboardView.urls(
    namespace=app_name,
    label="tmg_summary_listboard",
    identifier_pattern=subject_identifier,
)
urlpatterns += SubjectReviewListboardView.urls(
    namespace=app_name,
    label="subject_review_listboard",
    identifier_pattern=subject_identifier,
)
urlpatterns += AeListboardView.urls(
    namespace=app_name, label="ae_listboard", identifier_pattern=subject_identifier
)
urlpatterns += DeathReportListboardView.urls(
    namespace=app_name,
    label="death_report_listboard",
    identifier_pattern=subject_identifier,
)
