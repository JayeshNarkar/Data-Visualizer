from django import forms

class UploadForm(forms.Form):
    CHOICES = [(i, str(i)) for i in range(1, 5)]  # Choices 1 to 4

    file = forms.FileField(label='Upload CSV File', 
                           widget=forms.ClearableFileInput(attrs={'id': 'fileUpload', 'accept': '.csv', 'class': 'm-3'}))

    label_upload = forms.ChoiceField(label='Labels', choices=CHOICES)
    data_upload = forms.ChoiceField(label='Dataset', choices=CHOICES, widget=forms.Select(attrs={'id': 'dataUpload', 'class': 'mr-3'}))

    dataset_name = forms.CharField(label='DataSet Name:', max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        label_upload = cleaned_data.get('label_upload')
        data_upload = cleaned_data.get('data_upload')

        # Check if data and labels are the same
        if label_upload == data_upload:
            raise forms.ValidationError("Labels and Dataset numbers cannot be the same.")

        return cleaned_data
