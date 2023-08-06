import calendar

class Neptu():

    def convert_date(day, month, year):

        kabisat = year%4
        is_baisat = True if kabisat==0 else False

        decreased_month = month-1
        decreased_year = year-1

        cycle = int(decreased_year / 4)
        mod_cycle = decreased_year % 4

        cycle_days = cycle * 1461
        mod_cycle_days = mod_cycle * 365

        list_month_days = [
            calendar.monthrange(year, 1)[1],
            calendar.monthrange(year, 2)[1],
            calendar.monthrange(year, 3)[1],
            calendar.monthrange(year, 4)[1],
            calendar.monthrange(year, 5)[1],
            calendar.monthrange(year, 6)[1],
            calendar.monthrange(year, 7)[1],
            calendar.monthrange(year, 8)[1],
            calendar.monthrange(year, 9)[1],
            calendar.monthrange(year, 10)[1],
            calendar.monthrange(year, 11)[1],
            calendar.monthrange(year, 12)[1],
        ]

        total_month_days = 0

        for i in range(0, decreased_month):
            total_month_days = total_month_days + list_month_days[i]

        total_days = cycle_days + mod_cycle_days + total_month_days + day

        num_day = total_days%7
        num_pasaran = total_days%5

        list_days = ['Setu', 'Minggu', 'Senen', 'Seleasa', 'Rebo', 'Kemis', 'Jumat', 'Setu', 'Minggu']
        list_pasarans = ['Legi', 'Pahing', 'Pon', 'Wage', 'Kliwon']

        gregorian_correction = total_days - 227016 - 13

        cycle_convertion = int(gregorian_correction/10631)
        mod_cycle_convertion = gregorian_correction%10631

        year_convertion = cycle_convertion*30

        x=0
        for d in range((year-cycle_convertion), year):
            if d % 4 == 0:
                if d % 100 ==0:
                    if d % 400 == 0:
                        x = x+1
                else:
                    x=x+1


        day_date = (mod_cycle_convertion%10631)%(10631/30)

        list_months = ['Sura', 'Sapar', 'Mulud', 'Bakdamulud', 'Jumadilawal', 'Jumadilakhir', 'Rejeb', 'Ruwah', 'Pasa', 'Sawal', 'Sela', 'Besar']



        data = {
            'day': int(day_date%29.5),
            'month': int(day_date/29.5)+1,
            'month_name': list_months[int(day_date/29.5)],
            'day_name': list_days[num_day],
            'pasaran': list_pasarans[num_pasaran],
            'year': year_convertion+int(mod_cycle_convertion/(10631/30))+1,
        }

        return data