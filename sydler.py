import datetime

from sydler.utils.populate import Populate
from sydler.utils.excel_file_generator import ExcelFileGenerator

day = datetime.date(2019, 4, 9)
dates = [day]

days_to_add = 5
for index in range(1, 32):
    day = day + datetime.timedelta(days=days_to_add)
    dates.append(day)
    days_to_add = 2 if days_to_add == 5 else 5

populate = Populate(dates)
file_generator = ExcelFileGenerator(populate.get_assignments())
file_generator.make_excel()
