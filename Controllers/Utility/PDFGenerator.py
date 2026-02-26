"""
Utility/PDFGenerator.py
PDF report generation utilities with SAFE pie chart (with fallback)
"""
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

# Try to import chart libraries - if they fail, we'll use text-based fallback
CHARTS_AVAILABLE = True
try:
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.piecharts import Pie
except ImportError:
    CHARTS_AVAILABLE = False
    print("Chart libraries not available - will use text-based visualization")


class PDFGenerator:
    """Helper class for generating PDF reports"""

    @staticmethod
    def _create_safe_pie_chart(paid_count, unpaid_count):
        """Create a pie chart with error handling"""
        try:
            if not CHARTS_AVAILABLE:
                return None

            drawing = Drawing(250, 200)

            pie = Pie()
            pie.x = 50
            pie.y = 20
            pie.width = 150
            pie.height = 150
            pie.data = [paid_count, unpaid_count]
            pie.labels = ['Paid', 'Unpaid']
            pie.slices.strokeWidth = 0.5

            # Set colors - GREEN for paid, RED for unpaid
            pie.slices[0].fillColor = colors.HexColor('#27ae60')
            pie.slices[1].fillColor = colors.HexColor('#e74c3c')

            # Add percentage labels
            total = paid_count + unpaid_count
            if total > 0:
                for i in range(len(pie.slices)):
                    pie.slices[i].labelRadius = 1.35
                    pie.slices[i].fontColor = colors.black
                    pie.slices[i].fontSize = 11
                    pie.slices[i].fontName = 'Helvetica-Bold'

            drawing.add(pie)
            return drawing

        except Exception as e:
            print(f"Pie chart creation failed: {e}")
            return None

    @staticmethod
    def _create_text_based_visual(paid_count, unpaid_count, total_violations):
        """Fallback text-based visualization"""
        paid_percentage = (paid_count / total_violations * 100) if total_violations > 0 else 0
        unpaid_percentage = (unpaid_count / total_violations * 100) if total_violations > 0 else 0

        # Each █ = 5% (max 20 blocks)
        paid_bar = '█' * int(paid_percentage / 5)
        unpaid_bar = '█' * int(unpaid_percentage / 5)

        visual_data = [
            ['Payment Status', 'Visual', 'Count', 'Percentage'],
            ['PAID', paid_bar, str(paid_count), f"{paid_percentage:.1f}%"],
            ['UNPAID', unpaid_bar, str(unpaid_count), f"{unpaid_percentage:.1f}%"]
        ]

        visual_table = Table(visual_data, colWidths=[1.5 * inch, 2.5 * inch, 1.0 * inch, 1.2 * inch])
        visual_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            # Paid row
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#d4edda')),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#27ae60')),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 1), (1, 1), 14),

            # Unpaid row
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8d7da')),
            ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#e74c3c')),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 2), (1, 2), 14),

            # General styling
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2c3e50')),
        ]))

        return visual_table

    @staticmethod
    def generate_violations_report(file_path: str, violations: list):
        """
        Generate PDF report for violations with SAFE pie chart

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

            # ============= VISUAL SUMMARY =============
            visual_heading = Paragraph("VISUAL SUMMARY", heading_style)
            elements.append(visual_heading)
            elements.append(Spacer(1, 0.1 * inch))

            if total_violations > 0:
                # TRY to create pie chart, fallback to text if it fails
                pie_chart = PDFGenerator._create_safe_pie_chart(paid_count, unpaid_count)

                if pie_chart is not None:
                    # Pie chart worked! Use it
                    chart_table = Table([[pie_chart]], colWidths=[6.5 * inch])
                    chart_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    elements.append(chart_table)

                    # Legend for pie chart
                    legend_text = (
                        f"<b>Green</b> = Paid ({paid_count} violations, {(paid_count/total_violations*100):.1f}%) | "
                        f"<b>Red</b> = Unpaid ({unpaid_count} violations, {(unpaid_count/total_violations*100):.1f}%)"
                    )
                    legend = Paragraph(legend_text, normal_style)
                    elements.append(Spacer(1, 0.1 * inch))
                    elements.append(legend)
                else:
                    # Pie chart failed - use text-based visualization
                    text_visual = PDFGenerator._create_text_based_visual(
                        paid_count, unpaid_count, total_violations
                    )
                    elements.append(text_visual)

                elements.append(Spacer(1, 0.2 * inch))

                # Revenue summary
                revenue_summary = Paragraph(
                    f"<b>Revenue Summary:</b> Collected: ₱{total_revenue:,.2f} | "
                    f"Pending: ₱{pending_revenue:,.2f} | "
                    f"Total Potential: ₱{(total_revenue + pending_revenue):,.2f}",
                    normal_style
                )
                elements.append(revenue_summary)
                elements.append(Spacer(1, 0.3 * inch))

            # ============= VIOLATIONS TABLE =============
            # Page break before table for better layout
            elements.append(PageBreak())

            # Violations Table Header
            table_heading = Paragraph("DETAILED VIOLATIONS RECORDS", heading_style)
            elements.append(table_heading)
            elements.append(Spacer(1, 0.2 * inch))

            table_data = [
                ['ID', 'Resident', 'Contact', 'Plate', 'Vehicle', 'Violation',
                 'Date', 'Fine', 'Status', 'Paid Date']
            ]

            # Add violation data with FIXED paid date logic
            for v in violations:
                vehicle_info = f"{v['Brand']} {v['Model']}" if v['Brand'] and v['Model'] else 'N/A'
                contact = v['ContactNo'] if v['ContactNo'] else 'N/A'

                # FIXED: Only show payment date if status is PAID
                if v['PaymentStatus'] == 'PAID' and v.get('PaymentDate'):
                    payment_date = str(v['PaymentDate'])
                else:
                    payment_date = '-'

                table_data.append([
                    str(v['ViolationID']),
                    str(v['ResidentName'])[:20],
                    str(contact),
                    str(v['PlateNo']),
                    vehicle_info[:15],
                    str(v['ViolationName'])[:20],
                    str(v['ViolationDate']),
                    f"₱{float(v['FineAmount']):,.0f}",
                    str(v['PaymentStatus']),
                    payment_date
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
                f"Report contains {total_violations} violation record(s) | "
                f"Paid: {paid_count} | Unpaid: {unpaid_count}",
                footer_style
            )
            elements.append(footer)

            # Build PDF
            doc.build(elements)

            return True, f"PDF generated successfully with {total_violations} records"

        except Exception as e:
            return False, f"PDF generation error: {str(e)}"