from django.db import models


class CommonColumns(models.Model):
    class Meta:
        abstract = True
        
    f_binary = models.BinaryField(null=True)
    f_boolean = models.NullBooleanField(null=True)
    f_string = models.CharField(max_length=255, null=True)
    f_text = models.TextField(null=True)
    f_integer = models.IntegerField(null=True)
    f_float = models.FloatField(null=True)
    f_date = models.DateField(null=True)
    f_time = models.TimeField(null=True)
    f_datetime = models.DateTimeField(null=True)


class ModelMergeOne(CommonColumns):
    class Meta:
        db_table = 'model_merge_one'
    
    two_1_1 = models.OneToOneField('ModelMergeTwo',
                                   on_delete=models.CASCADE,
                                   related_name='one_1_1',
                                   null=True)
    two_x_1 = models.ForeignKey('ModelMergeTwo',
                                on_delete=models.CASCADE,
                                related_name='one_1_x',
                                null=True)


class ModelMergeTwo(CommonColumns):
    class Meta:
        db_table = 'model_merge_two'
    
    three_1_1 = models.OneToOneField('ModelMergeThree',
                                   on_delete=models.CASCADE,
                                   related_name='two_1_1',
                                   null=True)
    three_x_1 = models.ForeignKey('ModelMergeThree',
                                  on_delete=models.CASCADE,
                                  related_name='two_1_x',
                                  null=True)


class ModelMergeThree(CommonColumns):
    class Meta:
        db_table = 'model_merge_three'
        

class ModelMergeOneX(CommonColumns):
    class Meta:
        db_table = 'model_merge_one_x'
        unique_together = (('f_integer', 'two_x_1'),)

    two_x_1 = models.ForeignKey('ModelMergeTwoX',
                                on_delete=models.CASCADE,
                                related_name='one_1_x',
                                null=True)


class ModelMergeTwoX(CommonColumns):
    class Meta:
        db_table = 'model_merge_two_x'
        unique_together = (('f_integer', 'three_x_1'),)

    three_x_1 = models.ForeignKey('ModelMergeThreeX',
                                  on_delete=models.CASCADE,
                                  related_name='two_1_x',
                                  null=True)


class ModelMergeThreeX(CommonColumns):
    class Meta:
        db_table = 'model_merge_three_x'
        