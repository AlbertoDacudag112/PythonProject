"""
Utility/PDFGenerator.py
PDF report generation utilities (extracted from ReportsPage.py)
"""
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER


class PDFGenerator:
    """Helper class for generating PDF reports"""

    @staticmethod
    def generate_violations_report(file_path: str, violations: list):
        """
        Generate PDF report for violations

        Args:
            file_path: Path where PDF will be saved
            violations: List of violation dictionaries
        """
        try:
            # Calculate statistics
            total_violations = len(violations)
            paid_count = sum(1 for v in violations if v['PaymentStatus'] == 'PAID')
            unpaid_count = total_violations - paid_count
            total_revenue = sum(float(v['FineAmount']) for v in violations if v['PaymentStatus'] == 'PAID')
            pending_revenue = sum(float(v['FineAmount']) for v in violations if v['PaymentStatus'] != 'PAID')

            # Create PDF document in landscape mode
            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )

            # Container for PDF elements
            elements = []

            # Define styles
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )

            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER
            )

            # Title
            title = Paragraph("VIOLATIONS REPORT", title_style)
            elements.append(title)

            # Generated date
            date_info = Paragraph(
                f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>"
                f"<b>RoadEye - Vehicle Violation Monitoring System</b>",
                normal_style
            )
            elements.append(date_info)
            elements.append(Spacer(1, 0.3 * inch))

            # Summary Statistics Box
            summary_heading = Paragraph("SUMMARY STATISTICS", heading_style)
            elements.append(summary_heading)

            # Summary table
            summary_data = [
                ['Total Violations', str(total_violations), 'Paid Violations',
                 f"{paid_count} ({(paid_count / total_violations * 100) if total_violations > 0 else 0:.1f}%)"],
                ['Unpaid Violations',
                 f"{unpaid_count} ({(unpaid_count / total_violations * 100) if total_violations > 0 else 0:.1f}%)",
                 'Total Revenue', f"₱{total_revenue:,.2f}"],
                ['Pending Revenue', f"₱{pending_revenue:,.2f}",
                 'Total Potential', f"₱{(total_revenue + pending_revenue):,.2f}"]
            ]

            summary_table = Table(summary_data, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#2c3e50')),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3 * inch))

            # Violations Table Header
            table_data = [
                ['ID', 'Resident', 'Contact', 'Plate', 'Vehicle', 'Violation',
                 'Date', 'Fine', 'Status', 'Paid Date']
            ]

            # Add violation data
            for v in violations:
                vehicle_info = f"{v['Brand']} {v['Model']}" if v['Brand'] and v['Model'] else 'N/A'
                contact = v['ContactNo'] if v['ContactNo'] else 'N/A'
                payment_date = v['PaymentDate'] if v['PaymentDate'] else '-'

                table_data.append([
                    str(v['ViolationID']),
                    str(v['ResidentName'])[:20],  # Truncate long names
                    str(contact),
                    str(v['PlateNo']),
                    vehicle_info[:15],  # Truncate long vehicle names
                    str(v['ViolationName'])[:20],
                    str(v['ViolationDate']),
                    f"₱{float(v['FineAmount']):,.0f}",
                    str(v['PaymentStatus']),
                    str(payment_date)
                ])

            # Create violations table
            violations_table = Table(table_data, colWidths=[
                0.5 * inch, 1.2 * inch, 0.9 * inch, 0.7 * inch, 1.0 * inch,
                1.2 * inch, 0.8 * inch, 0.8 * inch, 0.7 * inch, 0.8 * inch
            ])

            # Style the table
            table_style = TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),

                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),

                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#aaaaaa')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2c3e50')),

                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ])

            # Color code the status column
            for i, row in enumerate(table_data[1:], start=1):
                if row[8] == 'PAID':
                    table_style.add('TEXTCOLOR', (8, i), (8, i), colors.HexColor('#27ae60'))
                    table_style.add('FONTNAME', (8, i), (8, i), 'Helvetica-Bold')
                else:
                    table_style.add('TEXTCOLOR', (8, i), (8, i), colors.HexColor('#e74c3c'))
                    table_style.add('FONTNAME', (8, i), (8, i), 'Helvetica-Bold')

            violations_table.setStyle(table_style)
            elements.append(violations_table)

            # Footer
            elements.append(Spacer(1, 0.3 * inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#666666')
            )
            footer = Paragraph(
                f"<b>RoadEye - Vehicle Violation Monitoring System</b><br/>"
                f"This is a computer-generated document. No signature required.<br/>"
                f"Report contains {total_violations} violation record(s)",
                footer_style
            )
            elements.append(footer)

            # Build PDF
            doc.build(elements)

            return True, f"PDF generated successfully with {total_violations} records"

        except Exception as e:
            return False, f"PDF generation error: {str(e)}"