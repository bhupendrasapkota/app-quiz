from rest_framework import serializers
from .models import Option, Question


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'isCorrect']
        required = ['option', 'isCorrect']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'category', 'level', 'options']
        required = ['question', 'category', 'level', 'options']

    def create(self, validated_data):
        options = validated_data.pop('options')
        question = Question.objects.create(**validated_data)

        for option in options:
            Option.objects.create(questionId=question, **option)

        return question
    
    class QuestionListSerializer(serializers.ModelSerializer):
        QuestionList = serializers.SerializerMethodField()
        class Meta:
            model = Question
            fields = ['id', 'question', 'isCorrect']

class QuizAttemptSerializer(serializers.ModelSerializer):
    question_attempt = QuestionAttemptSerializer(many=True)
    class Meta:
        model = QuizAttempt
        fields = ['id', 'attempted_date', 'total_score', 'question_attempt']
        
    def create(self, validated_data,context):
        user = context['request'].user
        quiz_attempt = QuizAttempt.objects.create(user=user)
        
        questions =list(Question.objects.all().order_by('?')[:20])
        
        for question in questions:
            QuestionAttempt.objects.create(attempt=quiz_attempt, question=question)
        return quiz_attempt
