from io import BytesIO
from fpdf import FPDF
from backend.application.interfaces.report_generator import ReportGenerator
from backend.application.dtos import ProcessCsvOutput

class PdfReportGenerator(ReportGenerator):
    def generate_report(self, output_dto: ProcessCsvOutput) -> BytesIO:
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()

        pdf.set_font('Arial', 'B', size=16)
        pdf.cell(w=0, h=10, text="Business Metrics Report", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font('Arial', 'B', size=12)
        pdf.cell(w=60, h=8, text="Metric", border=1)
        pdf.cell(w=0, h=8, text="Value", border=1, ln=True)

        pdf.set_font('Arial', size=12)
        pdf.cell(w=60, h=8, text="Total Revenue", border=1)
        pdf.cell(w=0, h=8, text=f"${output_dto.total_revenue:,.2f}", border=1, ln=True)

        pdf.cell(w=60, h=8, text="MoM Growth (%)", border=1)
        pdf.cell(w=0, h=8, text=f"{output_dto.mom_growth_rate:.2f}%", border=1, ln=True)

        pdf.cell(w=60, h=8, text="Avg. Ticket", border=1)
        pdf.cell(w=0, h=8, text=f"${output_dto.average_ticket:,.2f}", border=1, ln=True)

        pdf.cell(w=60, h=8, text="New Leads", border=1)
        pdf.cell(w=0, h=8, text=str(output_dto.total_leads), border=1, ln=True)

        pdf.ln(10)
        pdf.set_font('Arial', 'B', size=14)
        pdf.cell(w=0, h=10, text="Monthly Revenue", ln=True)
        pdf.ln(2)

        pdf.set_font('Arial', 'B', size=12)
        pdf.cell(w=50, h=8, text="Month", border=1)
        pdf.cell(w=0, h=8, text="Revenue", border=1, ln=True)

        pdf.set_font('Arial', size=12)
        for month, revenue in output_dto.monthly_revenue.items():
            pdf.cell(w=50, h=8, text=month, border=1)
            pdf.cell(w=0, h=8, text=f"${revenue:,.2f}", border=1, ln=True)

        pdf_bytes = bytes(pdf.output(dest='S'))

        output_buffer = BytesIO(pdf_bytes)

        return output_buffer
