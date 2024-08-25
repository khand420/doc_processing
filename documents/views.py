# documents/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document, ExtractedText, AIResult
from .forms import DocumentForm
import pytesseract
from PIL import Image
import spacy
from django.contrib.auth import login
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('upload_document')  # Redirect to the document upload page or another page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})





# Load spaCy model
nlp = spacy.load("en_core_web_sm")

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            
            # Process OCR
            extracted_text = process_ocr(document)
            
            # Process AI
            process_ai(extracted_text)

            return redirect('document_detail', document_id=document.id)
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

def process_ocr(document):
    # Assuming it's an image; for PDFs, you'll need to extract pages first
    img = Image.open(document.file.path)
    text = pytesseract.image_to_string(img)
    
    # Save extracted text
    extracted_text = ExtractedText.objects.create(document=document, text=text)
    return extracted_text


# from transformers import pipeline
# from textblob import TextBlob

# def process_ai(extracted_text):
#     # Perform Named Entity Recognition (NER)
#     doc = nlp(extracted_text.text)
#     entities = [{ "text": ent.text, "label": ent.label_ } for ent in doc.ents]

#     # Text Classification using Hugging Face's pipeline (e.g., for topic classification)
#     classifier = pipeline("text-classification")
#     classification_results = classifier(extracted_text.text)
#     classifications = [result['label'] for result in classification_results]

#     # Sentiment Analysis using TextBlob
#     sentiment = TextBlob(extracted_text.text).sentiment
#     sentiment_score = sentiment.polarity
#     sentiment_label = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"

#     # Save the AI results in the database
#     AIResult.objects.create(
#         document=extracted_text.document,
#         entities=entities,
#         classifications=classifications,
#         sentiment=sentiment_label
#     )


def process_ai(extracted_text):
    doc = nlp(extracted_text.text)
    
    entities = [{ "text": ent.text, "label": ent.label_ } for ent in doc.ents]
    
    # You can also add classification or sentiment analysis here
    AIResult.objects.create(
        document=extracted_text.document,
        entities=entities,
        classifications="",
        sentiment=""
    )

@login_required
def document_detail(request, document_id):
    document = Document.objects.get(id=document_id)
    extracted_text = ExtractedText.objects.get(document=document)
    ai_result = AIResult.objects.get(document=document)
    return render(request, 'document_detail.html', {
        'document': document,
        'extracted_text': extracted_text,
        'ai_result': ai_result,
    })
