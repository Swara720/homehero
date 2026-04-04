from django import forms
from .models import Service, Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500',
                'placeholder': 'e.g. Deep House Cleaning'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500',
                'rows': 5,
                'placeholder': 'Describe your service...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500',
                'placeholder': 'Enter price in rupees'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-2xl focus:outline-none focus:border-blue-500'
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1,6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }