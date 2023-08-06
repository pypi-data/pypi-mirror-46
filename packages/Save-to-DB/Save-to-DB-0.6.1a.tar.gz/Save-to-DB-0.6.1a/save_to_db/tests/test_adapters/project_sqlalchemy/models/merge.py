import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from ..config import Base



class __CommonColumns(object):
    id = sa.Column(sa.Integer, primary_key=True)
    
    f_binary = sa.Column(sa.LargeBinary, nullable=True)
    f_boolean = sa.Column(sa.Boolean, nullable=True)
    f_string = sa.Column(sa.String, nullable=True)
    f_text = sa.Column(sa.Text, nullable=True)
    f_integer = sa.Column(sa.Integer, nullable=True)
    f_float = sa.Column(sa.Float, nullable=True)
    f_date = sa.Column(sa.Date, nullable=True)
    f_time = sa.Column(sa.Time, nullable=True)
    f_datetime = sa.Column(sa.DateTime, nullable=True)
    
    __mapper_args__ = {
        'order_by': 'id',
    }



class ModelMergeOne(__CommonColumns, Base):
    __tablename__ = 'model_merge_one'
    
    two_1_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_two.id', ondelete='CASCADE'),
        unique=True)
    two_1_1 = relationship(
        'ModelMergeTwo',
        back_populates='one_1_1',
        foreign_keys=[two_1_1_id])
    
    two_x_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_two.id', ondelete='CASCADE'))
    two_x_1 = relationship(
        'ModelMergeTwo',
        back_populates='one_1_x',
        foreign_keys=[two_x_1_id])


class ModelMergeTwo(__CommonColumns, Base):
    __tablename__ = 'model_merge_two'
    
    one_1_1 = relationship(
        'ModelMergeOne',
        back_populates='two_1_1',
        foreign_keys='[ModelMergeOne.two_1_1_id,]',
        uselist=False)
    one_1_x = relationship(
        'ModelMergeOne',
        back_populates='two_x_1',
        foreign_keys='[ModelMergeOne.two_x_1_id,]',)
    
    three_1_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_three.id', ondelete='CASCADE'),
        unique=True)
    three_1_1 = relationship(
        'ModelMergeThree',
        back_populates='two_1_1',
        foreign_keys=[three_1_1_id])
    
    three_x_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_three.id', ondelete='CASCADE'))
    three_x_1 = relationship(
        'ModelMergeThree',
        back_populates='two_1_x',
        foreign_keys=[three_x_1_id])


class ModelMergeThree(__CommonColumns, Base):
    __tablename__ = 'model_merge_three'
    
    two_1_1 = relationship(
        'ModelMergeTwo',
        back_populates='three_1_1',
        foreign_keys='[ModelMergeTwo.three_1_1_id,]',
        uselist=False)
    two_1_x = relationship(
        'ModelMergeTwo',
        back_populates='three_x_1',
        foreign_keys='[ModelMergeTwo.three_x_1_id,]',)


class ModelMergeOneX(__CommonColumns, Base):
    __tablename__ = 'model_merge_one_x'

    two_x_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_two_x.id', ondelete='CASCADE'))
    two_x_1 = relationship(
        'ModelMergeTwoX',
        back_populates='one_1_x',
        foreign_keys=[two_x_1_id])
    
    __table_args__ = (
        UniqueConstraint('two_x_1_id', 'f_integer', name='unique_1'),
    )


class ModelMergeTwoX(__CommonColumns, Base):
    __tablename__ = 'model_merge_two_x'

    one_1_x = relationship(
        'ModelMergeOneX',
        back_populates='two_x_1',
        foreign_keys='[ModelMergeOneX.two_x_1_id,]',)
    
    three_x_1_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('model_merge_three_x.id', ondelete='CASCADE'))
    three_x_1 = relationship(
        'ModelMergeThreeX',
        back_populates='two_1_x',
        foreign_keys=[three_x_1_id])
    
    __table_args__ = (
        UniqueConstraint('three_x_1_id', 'f_integer', name='unique_1'),
    )


class ModelMergeThreeX(__CommonColumns, Base):
    __tablename__ = 'model_merge_three_x'

    two_1_x = relationship(
        'ModelMergeTwoX',
        back_populates='three_x_1',
        foreign_keys='[ModelMergeTwoX.three_x_1_id,]',)
    