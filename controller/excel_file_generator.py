import datetime
import openpyxl
from openpyxl.styles import Font
from openpyxl.styles import Alignment
# from openpyxl.styles import PatternFill

from controller.populate import Populate


class ExcelFileGenerator:

    def __init__(self, assignment_queue):
        self.__assignment_queue = assignment_queue
        self.__workbook = openpyxl.Workbook()
        self.active_sheet = self.__workbook.get_active_sheet()

    def fill_header_info(self):
        a1 = self.active_sheet['A1']
        a1.value = 'ADDIS SEFER CONGREGATION\nSOUND SYSTEM SCHEDULE'
        self.active_sheet.merge_cells('A1:H1')
        title_font = Font(size=25, bold=True)
        title_alignment = Alignment(horizontal="center", vertical="center")
        a1.font = title_font
        a1.alignment = title_alignment

    def make_excel(self):
        self.fill_header_info()
        self.fill_column_titles()
        self.fill_week_spans()
        self.set_page_properties()
        self.complete_generation()

    def fill_column_titles(self):
        week_span_column_title = 'ሳምንት'
        week_span_title_cell = 'A2'
        self.active_sheet[week_span_title_cell] = week_span_column_title

        meeting_day_name_column_title = 'ቀን'
        meeting_day_title_cell = 'B2'
        self.active_sheet[meeting_day_title_cell] = meeting_day_name_column_title

        stage_column_title = 'መድረክ'
        stage_title_cell = 'C2'
        self.active_sheet[stage_title_cell] = stage_column_title

        mic_first_round_title = 'የመጀመሪያ ዙር'
        mic_first_round_title_cell = 'D2'
        self.active_sheet[mic_first_round_title_cell] = mic_first_round_title

        mic_second_round_title = 'ሁለተኛ ዙር'
        mic_second_round_title_cell = 'F2'
        self.active_sheet[mic_second_round_title_cell] = mic_second_round_title

        second_hall_title_title = 'ሁለተኛ አዳራሽ'
        second_hall_title_cell = 'H2'
        self.active_sheet[second_hall_title_cell] = second_hall_title_title

    def fill_week_spans(self):
        program_dates = []

        for _assignment in self.__assignment_queue:
            program_dates.append(_assignment.assignment_date)

        row = 2
        for _date in sorted(program_dates):
            row += 1
            cell = 'A' + str(row)
            self.active_sheet[cell].value = _date

    def set_page_properties(self):
        self.active_sheet.paper_size = 'A4'

    def complete_generation(self):
        self.active_sheet.paper_size = self.active_sheet.PAPERSIZE_A4
        self.__workbook.save("schedule.xlsx")


day = datetime.datetime.now()
dates = [
    day + datetime.timedelta(days=1),
    day + datetime.timedelta(days=2),
    day + datetime.timedelta(days=3),
    day + datetime.timedelta(days=4),
    day + datetime.timedelta(days=5),
    day + datetime.timedelta(days=6),
    day + datetime.timedelta(days=7),
    day + datetime.timedelta(days=8),
    day + datetime.timedelta(days=9),
    day + datetime.timedelta(days=10),
    day + datetime.timedelta(days=11),
    day + datetime.timedelta(days=12)
]

populate = Populate(dates)
file_generator = ExcelFileGenerator(populate.get_assignments())
file_generator.make_excel()
