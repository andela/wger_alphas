# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from rest_framework import serializers
from wger.exercises.models import (
    Muscle,
    Exercise,
    ExerciseImage,
    ExerciseCategory,
    Equipment,
    ExerciseComment
)


class MuscleSerializer(serializers.ModelSerializer):
    '''
    Muscle serializer
    '''
    name = serializers.CharField()

    class Meta:
        model = Muscle
        fields = ('id', 'name', 'is_front')


class EquipmentSerializer(serializers.ModelSerializer):
    '''
    Equipment serializer
    '''
    class Meta:
        model = Equipment
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):
    '''
    Exercise serializer
    '''
    name = serializers.CharField()
    category = serializers.StringRelatedField()
    description = serializers.CharField(source='description_clean')
    muscles = serializers.SlugRelatedField(many=True,
                                           read_only=True,
                                           slug_field='name')
    # Alternative to serialize all muscles attributes
    # muscles = MuscleSerializer(many=True, read_only=True)
    muscles_secondary = serializers.SlugRelatedField(many=True,
                                                     read_only=True,
                                                     slug_field='name')
    # Alternative to serialize all secondary_muscles attributes
    # muscles_secondary = MuscleSerializer(many=True, read_only=True)
    equipment = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='name')
    # Alternative to serialize all equipment attributes
    # equipment = EquipmentSerializer(many=True, read_only=True)
    status = serializers.CharField(source='status_description')
    language = serializers.StringRelatedField()
    license = serializers.StringRelatedField()

    class Meta:
        model = Exercise


class ExerciseCategorySerializer(serializers.ModelSerializer):
    '''
    ExerciseCategory serializer
    '''
    class Meta:
        model = ExerciseCategory


class ExerciseImageSerializer(serializers.ModelSerializer):
    '''
    ExerciseImage serializer
    '''
    class Meta:
        model = ExerciseImage


class ExerciseCommentSerializer(serializers.ModelSerializer):
    '''
    ExerciseComment serializer
    '''
    class Meta:
        model = ExerciseComment
