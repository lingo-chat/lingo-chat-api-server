from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import create_engine, BigInteger, Float, TIMESTAMP

from sqlalchemy.orm import relationship

from .database import Base


class OpenModelList(Base):
    __tablename__ = "open_model_list"
    
    model_id = Column(String, primary_key=True, index=True)
    
    model_name = Column(String)
    size = Column(String)
    base_model_name = Column(String)
    model_version = Column(String, nullable=True)
    update_date = Column(TIMESTAMP, nullable=True)
    

class TrainDataset(Base):
    __tablename__ = "train_dataset"
    
    dataset_name = Column(String, primary_key=True, index=True)
    
    categories = Column(String)
    origin = Column(String)
    size = Column(String)
    language = Column(String)
    domain = Column(String)
    url = Column(String)


class PersonaInfo(Base):
    __tablename__ = "persona_info"
    
    persona_id = Column(String, primary_key=True, index=True)
    persona_name = Column(String)
    

class TunedModels(Base):
    __tablename__ = "tuned_models"
    
    tuned_model_id = Column(String, primary_key=True, index=True)
    
    model_id = Column(String, ForeignKey("open_model_list.model_id"), nullable=False)
    dataset_name = Column(String, ForeignKey("train_dataset.dataset_name"), nullable=False)
    persona_id = Column(String, ForeignKey("persona_info.persona_id"), nullable=False)
    
    dataset_categories = Column(String, nullable=True)
    tuned_model_version = Column(String)
    tuned_date = Column(TIMESTAMP, nullable=True)


class TrainingArguments(Base):
    __tablename__ = "training_arguments"
    
    tuned_model_id = Column(String, ForeignKey("tuned_models.tuned_model_id"), primary_key=True)
    
    tuned_categories = Column(String)
    epoch = Column(Integer, nullable=True)
    batch_size = Column(Integer, nullable=True)
    learning_rate = Column(Float, nullable=True)
    warmup_steps = Column(Integer, nullable=True)
    lr_scheduler = Column(String, nullable=True)
    optimizer = Column(String, nullable=True)
    wandb_link = Column(String, nullable=True)
    

class FeedbackInfo(Base):
    __tablename__ = "feedback_info"
    
    feedback_id = Column(BigInteger, primary_key=True, index=True)
    
    tuned_model_id = Column(Integer, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    log_id = Column(BigInteger, nullable=True)
    # log_id = Column(BigInteger, ForeignKey("qa_log.log_id"), nullable=False)
    
    feedback = Column(String, nullable=False)
    feedback_time = Column(TIMESTAMP)


class QALog(Base):
    __tablename__ = "qa_log"
    
    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(String, index=True, nullable=False)
    # log_id = Column(BigInteger, primary_key=True) # Sqlite에서 BigInteger는 무조건 설정해줘야 하는 값이 된다..
    
    tuned_model_id = Column(Integer, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    is_single_turn = Column(Boolean, nullable=False)
    user_id = Column(String, nullable=True)        # 랜덤 string 16자리 수
    chat_time = Column(TIMESTAMP, nullable=True)

    # user_questions = relationship("UserQuestion", back_populates="qa_log", cascade="all, delete-orphan")
    # model_answers = relationship("ModelAnswer", back_populates="qa_log", cascade="all, delete-orphan")


class UserQuestion(Base):
    __tablename__ = "user_question"
    
    # question_id = Column(Integer, ForeignKey("tuned_models.tuned_model_id"), primary_key=True, index=True, autoincrement=True)
    
    log_id = Column(Integer, ForeignKey("qa_log.log_id"), primary_key=True, nullable=False)
    question = Column(String(2048))

    # qa_log = relationship("QALog", back_populates="user_questions")


class ModelAnswer(Base):
    __tablename__ = "model_answer"
    
    # answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    log_id = Column(Integer, ForeignKey("qa_log.log_id"), primary_key=True, nullable=False)
    answer = Column(String(2048))
    response_gen_time_elapsed = Column(Integer, nullable=True)
    
    # qa_log = relationship("QALog", back_populates="model_answers")


class EvalModelList(Base):
    __tablename__ = "eval_model_list"
    
    llm_eval_name = Column(String, primary_key=True, index=True)
    api_request_url = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    update_date = Column(TIMESTAMP, nullable=True)
    

class LLMEvalResult(Base):
    __tablename__ = "llm_eval_result"
    
    eval_id = Column(Integer, primary_key=True, index=True)
    
    llm_eval_name = Column(String, ForeignKey("eval_model_list.llm_eval_name"), nullable=False)
    tuned_model_id = Column(Integer, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    
    persona_fidelity_score = Column(Integer, nullable=True)
    friendliness_score = Column(Integer, nullable=True)
    accuracy_score = Column(Integer, nullable=True)
    avg_score = Column(Integer, nullable=True)
    eval_time = Column(TIMESTAMP, nullable=True)


class WinVotes(Base):
    __tablename__ = "win_votes"
    
    win_votes_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_a_id = Column(String, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    model_b_id = Column(String, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    win_model = Column(String, ForeignKey("tuned_models.tuned_model_id"), nullable=False)
    
    total_votes = Column(Integer, index=True, autoincrement=True)
    vote_date = Column(TIMESTAMP, nullable=False)
