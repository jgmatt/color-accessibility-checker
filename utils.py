import numpy as np
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from daltonlens import convert, simulate, generate
from io import BytesIO
import ipywidgets as widgets
from IPython.display import display

def simulate_colorblindness(image, cb_type="deuteranopia", severity=1.0):
    """Apply colorblind filter to an image."""
    cb_filters = {
        "deuteranopia": simulate.Deficiency.DEUTAN,
        "protanopia": simulate.Deficiency.PROTAN,
        "tritanopia": simulate.Deficiency.TRITAN,
    }
    image = image.convert('RGB')
    # limit size
    MAX_WIDTH = 1000
    MAX_HEIGHT = 2000
    if image.width > MAX_WIDTH:
        image = image.resize((MAX_WIDTH, int(image.height * MAX_WIDTH / image.width)))
    if image.height > MAX_HEIGHT:
        image = image.resize((int(image.width * MAX_HEIGHT / image.height), MAX_HEIGHT))

    if cb_type in cb_filters:
      im = np.asarray(image.convert('RGB'))
      simulator = simulate.Simulator_Machado2009()
      filtered_im = simulator.simulate_cvd(im, cb_filters[cb_type], severity=severity)
      return Image.fromarray(filtered_im)
    elif cb_type == "grayscale":
      image = image.convert('L')
      return image
    else:
      raise ValueError(f"Unsupported colorblindness type: {cb_type}")

def process_images(input_files, cb_type="deuteranopia", severity=1.0, pdf_page=1):
  """Process various image formats and save as a PDF."""
  images = []
  for file in input_files:
      if file.lower().endswith(".pdf"):
          images.extend(convert_from_path(file, first_page=pdf_page, last_page=pdf_page))
      else:
          images.append(Image.open(file))
  filtered_images = [simulate_colorblindness(img, cb_type, severity) for img in images]
  return filtered_images

def upload_files():
  upload_widget = widgets.FileUpload(accept='.pdf,.jpg,.jpeg,.png,', multiple=True)
  display(upload_widget)
  return upload_widget

def settings_widgets():
  # Dropdown for colorblindness type
  cb_type_widget = widgets.Dropdown(
      options=['deuteranopia', 'protanopia', 'tritanopia', 'grayscale'],
      value='deuteranopia',
      description='CB Type:',
      style={'description_width': 'initial'}
  )

  # Slider for severity
  severity_widget = widgets.FloatSlider(
      value=1.0,
      min=0.0,
      max=1.0,
      step=0.01,
      description='Severity:',
      style={'description_width': 'initial'}
  )

  # IntText for PDF page selection
  pdf_page_widget = widgets.IntText(
      value=7,
      description='PDF Page:',
      style={'description_width': 'initial'}
  )

  return cb_type_widget, severity_widget, pdf_page_widget

def process_and_display(upload_widget, cb_type_widget, severity_widget, pdf_page_widget):
  if upload_widget.value:
    uploaded_files = []
    for uploaded_filename in upload_widget.value.keys():
        with open(uploaded_filename, "wb") as f:
            f.write(upload_widget.value[uploaded_filename]['content'])
        uploaded_files.append(uploaded_filename)

    # Access selected settings
    cb_type = cb_type_widget.value
    severity = severity_widget.value
    pdf_page = pdf_page_widget.value

    # Process all (simultaneously) uploaded images
    filtered_images = process_images(uploaded_files, cb_type, severity, pdf_page)

    # Display processed images
    for img in filtered_images:
        display(img)
        
  else:
    raise ValueError("You should upload a file first!")