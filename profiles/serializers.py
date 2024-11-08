from rest_framework import serializers
from .models import Profile, WorkHistory, Education, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = ['id', 'job_title', 'company_name',
                  'start_date', 'end_date', 'job_description']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution_name', 'degree',
                  'field_of_study', 'start_date', 'end_date']


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    work_history_entries = WorkHistorySerializer(many=True, read_only=True)
    education_entries = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
