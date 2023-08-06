# -*- coding: utf-8 -*-

from djangoplus.ui.components.forms import widgets


class CepWidget(widgets.MaskWidget):
    def __init__(self):
        super(CepWidget, self).__init__('00.000-000')

    def render(self, name, value=None, attrs=None, renderer=None):
        html = super(CepWidget, self).render(name, value, attrs)
        prefix = '-' in name and '{}-'.format(name.split('-')[0]) or ''
        function_name = prefix.replace('-', '__')
        js = """
        <script>
            $('#id_%(name)s').blur(function() {
                var cep = $('#id_%(name)s').val().replace('.', '').replace('-', '');
                if(cep && !window['executing_tests']){
                    $.getJSON("/enderecos/consultar/"+cep+"/", function( data ) {
                        if(data.message){
                            $.toast({ text: data.message, loader: false, position : 'top-right', hideAfter: 5000});
                        } else {
                            if(data.logradouro) $('#id_%(prefix)slogradouro').val(data.logradouro);
                            if(data.bairro) $('#id_%(prefix)sbairro').val(data.bairro);
                            if(data.cidade_id) load%(function_name)smunicipio(data.cidade_id, data.cidade);
                        }
                    });
                }
            });
        </script>
        """ % dict(name=name, prefix=prefix, function_name=function_name)
        return '{}{}'.format(html, js)

