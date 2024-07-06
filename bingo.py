import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_bingo_card(items):
    if len(items) < 24:
        raise ValueError("List must contain at least 24 items to fill the Bingo card (excluding the 'FREE' space).")

    random.shuffle(items)
    
    # Insert 'FREE' in the middle of the shuffled items
    items.insert(12, 'Gratuit!')
    
    # Split items into a 5x5 grid
    card = [items[i:i+5] for i in range(0, 25, 5)]
    return card

def create_bingo_table_data(card):
    data = []
    for row in card:
        data.append(row)
    return data

def custom_word_wrap(text, style, max_width):
    """
    Custom word wrap function to wrap text at word boundaries.
    """
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        # Try adding the word to the current line
        current_line.append(word)
        line_width = Paragraph(" ".join(current_line), style).wrap(max_width, 0)[0]

        # If adding the word exceeds the max_width, start a new line
        if line_width > max_width:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    return "<br/>".join(lines)

def create_bingo_pdf(cards, filename="bingo_cards.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    cell_size = 1.5 * inch  # Size of each cell (square)

    # Define a style sheet for paragraphs (text inside cells)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 18.5  # Initial font size
    style.leading = 20  # Line spacing (adjust as needed)
    style.allowWidows = 0  # Disable widows
    style.allowOrphans = 0  # Disable orphans

    for card in cards:
        table_data = create_bingo_table_data(card)
        table = Table(table_data, colWidths=[cell_size]*5, rowHeights=[cell_size]*5)

        # Add style to the table
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Update cell content with Paragraphs to handle multi-line text
        for i in range(len(card)):
            for j in range(len(card[i])):
                text = card[i][j]
                if isinstance(text, str):
                    text = text.strip()
                    if len(text) > 0:
                        wrapped_text = custom_word_wrap(text, style, cell_size)
                        para = Paragraph(wrapped_text, style)
                        if text == 'Gratuit!':
                            if text == 'Gratuit!':
                                bg_color = colors.lightgrey
                            else:
                                bg_color = colors.white
                        table._argW[j] = cell_size  # Ensure column width is maintained
                        table._argH[i] = cell_size  # Ensure row height is maintained
                        table._cellvalues[i][j] = para

        elements.append(table)
        elements.append(Spacer(1, 12))  # Add space between cards

    doc.build(elements)

if __name__ == "__main__":
    items = countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
        "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso",
        "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
        "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia",
        "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
        "East Timor (Timor-Leste)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
        "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
        "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
        "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
        "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia",
        "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
        "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
        "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru",
        "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
        "Oman", "Pakistan", "Palau", "Palestinian State*", "Panama", "Papua New Guinea", "Paraguay", "Peru",
        "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and The Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
        "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga",
        "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
        "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu",
        "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]

    num_cards = 30  # Number of bingo cards to generate
    cards = [generate_bingo_card(items[:]) for _ in range(num_cards)]
    create_bingo_pdf(cards)
