from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    """
    Using the plain serializer class we have to explecitly define each data type we want to
    serialize in our model and its data type.

    For our api to work we need to be able to input/output data from our db. Of course in this app
    everything is a python object which the browser cant understand. So we need to "serialize" the
    data into a string of text or json. If we want to write data from the browser to the db we need
    also convert the string of text into python objects. Thats what this serialzer is doing and why
    everything needs to be defined.

    For example our snippet model has a title field called title. So in the build up of this class
    we define a serializable field "title" = "char field"
    """

    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='fridssdsdsdeeeeendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        self.style = 'unfriendly'
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class SnippetModelSerializer(serializers.ModelSerializer):
    """
    Using the model serializer we can abstract some of the above code since the data types
    are already defined in our model, its safe to do.
    """

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

