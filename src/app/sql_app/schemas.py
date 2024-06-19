from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

###
class OpenModelListBase(BaseModel):
    model_name: str
    size: str
    base_model_name: str
    model_version: Optional[str] = None
    update_date: Optional[datetime] = None

class OpenModelListCreate(OpenModelListBase):
    model_id: str
    
class OpenModelList(OpenModelListBase):
    model_id: str

    class Config:
        orm_mode = True
        
###
class TrainDatasetBase(BaseModel):
    categories: str
    origin: str
    size: str
    language: str
    domain: str
    url: str

class TrainDatasetCreate(TrainDatasetBase):
    dataset_name: str

class TrainDataset(TrainDatasetBase):
    dataset_name: str

    class Config:
        orm_mode = True

###
class PersonaInfoBase(BaseModel):
    persona_name: str

class PersonaInfoCreate(PersonaInfoBase):
    persona_id: str

class PersonaInfo(PersonaInfoBase):
    persona_id: str
    
    class Config:
        orm_mode = True
        
###
class TunedModelsBase(BaseModel):
    model_id: str
    persona_id: str
    dataset_name: str
    dataset_categories: str
    tuned_model_version: str
    tuned_date: Optional[datetime] = None

class TunedModelsCreate(TunedModelsBase):
    tuned_model_id: str

class TunedModels(TunedModelsBase):
    tuned_model_id: str

    class Config:
        orm_mode = True

###
class TrainingArgumentsBase(BaseModel):
    tuned_categories: str
    epoch: Optional[int] = None
    batch_size: Optional[int] = None
    learning_rate: Optional[float] = None
    warmup_steps: Optional[int] = None
    lr_scheduler: Optional[str] = None
    optimizer: Optional[str] = None
    wandb_link: Optional[str] = None

class TrainingArgumentsCreate(TrainingArgumentsBase):
    tuned_model_id: str

class TrainingArguments(TrainingArgumentsBase):
    tuned_model_id: str

    class Config:
        orm_mode = True


###
class FeedbackInfoBase(BaseModel):
    tuned_model_id: str
    log_id: int
    feedback: str
    feedback_time: Optional[datetime] = None

class FeedbackInfoCreate(FeedbackInfoBase):
    feedback_id: int

class FeedbackInfo(FeedbackInfoBase):
    feedback_id: int

    class Config:
        orm_mode = True

###
class QALogBase(BaseModel):
    question_id: str
    tuned_model_id: str
    is_single_turn: bool
    user_id: str
    chat_time: Optional[datetime] = None

class QALogCreate(QALogBase):           # UserQuestion, ModelAnswer 유효성 검사
    question: str
    answer: str
    response_gen_time_elapsed: Optional[int] = None
    

class QALog(QALogBase):
    log_id: int     # autoincremental primary key
    # question_id: int

    class Config:
        orm_mode = True

###
class UserQuestionBase(BaseModel):
    question: str

class UserQuestionCreate(UserQuestionBase):
    pass

class UserQuestion(UserQuestionBase):
    log_id: int
    
    class Config:
        orm_mode = True

class ModelAnswerBase(BaseModel):
    log_id: int
    answer: str
    response_gen_time_elapsed: Optional[int] = None

class ModelAnswerCreate(ModelAnswerBase):
    pass

class ModelAnswer(ModelAnswerBase):

    class Config:
        orm_mode = True

### 
class EvalModelListBase(BaseModel):
    api_request_url: Optional[str] = None
    organization: Optional[str] = None
    model_version: Optional[str] = None
    update_date: Optional[datetime] = None

class EvalModelListCreate(EvalModelListBase):
    llm_eval_name: str

class EvalModelList(EvalModelListBase):
    llm_eval_name: str

    class Config:
        orm_mode = True
        
###
class LLMEvalResultBase(BaseModel):
    llm_eval_name: str
    tuned_model_id: str
    persona_fidelity_score: Optional[int] = None
    friendliness_score: Optional[int] = None
    accuracy_score: Optional[int] = None
    avg_score: Optional[int] = None
    eval_time: Optional[datetime] = None

class LLMEvalResultCreate(LLMEvalResultBase):
    eval_id: int

class LLMEvalResult(LLMEvalResultBase):
    eval_id: int

    class Config:
        orm_mode = True

###
class WinVotesBase(BaseModel):
    model_a_id: str
    model_b_id: str
    win_model: str
    
    vote_date: datetime

class WinVotesCreate(WinVotesBase):
    pass

class WinVotes(WinVotesBase):
    win_votes_id: int
    total_votes: int

    class Config:
        orm_mode = True
