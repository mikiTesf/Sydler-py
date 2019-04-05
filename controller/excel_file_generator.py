import datetime
import openpyxl
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill
from openpyxl.styles import Color

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
        title_font = Font(size=11, bold=True)
        alignment = Alignment(horizontal='center', vertical='center')
        fill_color = PatternFill(patternType='solid', fgColor=Color(rgb="AAAAAA"))

        week_span_column_title = 'ሳምንት'
        week_span_title_cell = 'A2'
        self.active_sheet[week_span_title_cell] = week_span_column_title

        meeting_day_name_column_title = 'ቀን'
        meeting_day_title_cell = 'B2'
        self.active_sheet[meeting_day_title_cell] = meeting_day_name_column_title

        stage_column_title = 'መድረክ'
        stage_title_cell = 'C2'
        self.active_sheet[stage_title_cell] = stage_column_title

        mic_first_round_title = 'በመጀመሪያ ዙር'
        mic_first_round_title_cell = 'D2'
        self.active_sheet[mic_first_round_title_cell] = mic_first_round_title
        self.active_sheet.merge_cells('D2:E2')

        mic_second_round_title = 'በሁለተኛ ዙር'
        mic_second_round_title_cell = 'F2'
        self.active_sheet[mic_second_round_title_cell] = mic_second_round_title
        self.active_sheet.merge_cells('F2:G2')

        second_hall_title_title = 'ሁለተኛ አዳራሽ'
        second_hall_title_cell = 'H2'
        self.active_sheet[second_hall_title_cell] = second_hall_title_title

        for column in range(1, 9):
            self.active_sheet.cell(2, column).font = title_font
            self.active_sheet.cell(2, column).alignment = alignment
            self.active_sheet.cell(2, column).fill = fill_color

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
        self.__workbook.save("../schedule.xlsx")


day = datetime.datetime.now()
dates = []

for days_to_add in range(1, 10):
    dates.append(day + datetime.timedelta(days=days_to_add))

populate = Populate(dates)
file_generator = ExcelFileGenerator(populate.get_assignments())
file_generator.make_excel()
