from edc_pdutils import CrfDfHandler as BaseCrfDfHandler
from edc_pdutils import NonCrfDfHandler as BaseNonCrfDfHandler

from .column_handlers import ColumnHandler


class CrfDfHandler(BaseCrfDfHandler):

    column_handler_cls = ColumnHandler
    na_value = "."

    visit_tbl = "ambition_subject_subjectvisit"
    enrollment_tbl = "ambition_screening_subjectscreening"
    rando_tbl = "ambition_rando_randomizationlist"
    sort_by = ["subject_identifier", "visit_datetime"]


class NonCrfDfHandler(BaseNonCrfDfHandler):

    column_handler_cls = ColumnHandler
    na_value = "."
