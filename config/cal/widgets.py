from django import forms

class RateitjsWidget(forms.NumberInput):
    input_type = 'rating'
    template_name ='cal/rateitjs_number.html'

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.update({
            'step': 1,
            'starwidth' :64,
            'starheight' : 64,
        })
        return attrs

