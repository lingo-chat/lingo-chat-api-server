import sys
sys.path.append("../")
from .. import models, schemas

from sqlalchemy.orm import Session

############ open_model_list ############

def get_opensource_model_info(db: Session, model_id: str):
    model_info = db.query(models.OpenModelList).filter(models.OpenModelList.model_id == model_id).first()
    if model_info is None:
        raise HTTPException(status_code=404, detail="Input opensource model is not found in DB.")
    return model_info

def get_model_name(db: Session, model_id: str):
    model_info = get_opensource_model_info(db, model_id)
    return model_info.model_name

def get_model_size(db: Session, model_id: str):
    model_info = get_opensource_model_info(db, model_id)
    return model_info.size

def get_base_model_name(db: Session, model_id: str):
    model_info = get_opensource_model_info(db, model_id)
    return model_info.base_model_name

def get_model_version(db: Session, model_id: str):
    model_info = get_opensource_model_info(db, model_id)
    return model_info.model_version

def get_model_update_date(db: Session, model_id: str):
    model_info = get_opensource_model_info(db, model_id)
    return model_info.update_date


############ train_dataset ############

def get_train_dataset_info(db: Session, dataset_name: str):
    dataset_info = db.query(models.TrainDataset).filter(models.TrainDataset.dataset_name == dataset_name).first()
    if dataset_info is None:
        raise HTTPException(status_code=404, detail="Input dataset is not found in DB.")
    return dataset_info

def get_dataset_categories(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.categories

def get_dataset_origin(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.origin

def get_dataset_size(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.size

def get_dataset_language(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.language

def get_dataset_domain(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.domain

def get_dataset_url(db: Session, dataset_name: str):
    dataset_info = get_train_dataset_info(db, dataset_name)
    return dataset_info.url


############ persona_info ############

def get_persona_info(db: Session, persona_id: str):
    persona_info = db.query(models.PersonaInfo).filter(models.PersonaInfo.persona_id == persona_id).first()
    if persona_info is None:
        raise HTTPException(status_code=404, detail="Input persona id is not found in DB.")
    return persona_info

def get_persona_name(db: Session, persona_id: str):
    persona_info = get_persona_info(db, persona_id)
    return persona_info.persona_name


############ tuned_models ############

def get_tuned_model_info(db: Session, tuned_model_id:str):
    tuned_model_info = db.query(models.TunedModels).filter(models.TunedModels.tuned_model_id == tuned_model_id).first()
    if tuned_model is None:
        raise HTTPException(status_code=404, detail="Input tuned model id is not found in DB.")
    return tuned_model_info

def get_tuned_model_dataset_name(db: Session, tuned_model_id: str):
    tuned_model = get_tuned_model_info(db, tuned_model_id)
    return tuned_model.dataset_name

def get_tuned_model_opensource_model_id(db: Session, tuned_model_id: str):
    tuned_model = get_tuned_model_info(db, tuned_model_id)
    return tuned_model.model_id

def get_tuned_model_persona_id(db: Session, tuned_model_id: str):
    tuned_model = get_tuned_model_info(db, tuned_model_id)
    return tuned_model.persona_id


############ feedback_info ############
def get_feedback_info(db: Session, feedback_id: int):
    feedback_info = db.query(models.FeedbackInfo).filter(models.FeedbackInfo.feedback_id == feedback_id).first()
    if feedback_info is None:
        raise HTTPException(status_code=404, detail="Input feedback id is not found in DB.")
    return feedback_info

# def get_feedback_log(db: Session, feedback_id: int):
#     feedback_info = get_feedback_info(db, feedback_id)
#     return feedback_info.feedback

def get_feedback_content(db: Session, feedback_id: int):
    feedback_info = get_feedback_info(db, feedback_id)
    return feedback_info.feedback

def get_feedback_time(db: Session, feedback_id: int):
    feedback_info = get_feedback_info(db, feedback_id)
    return feedback_info.feedback_time

def get_feedback_model_id(db: Session, feedback_id: int):
    feedback_info = get_feedback_info(db, feedback_id)
    return feedback_info.tuned_model_id


############ qa_log ############

def get_qa_log_info(db: Session, log_id: int):
    qa_log_info = db.query(models.QALog).filter(models.QALog.log_id == log_id).first()
    if qa_log_info is None:
        raise HTTPException(status_code=404, detail="Input qa log id is not found in DB.")
    return qa_log_info

def get_qa_log_user_questions(db: Session, log_id: int):
    qa_log_info = get_qa_log_info(db, log_id)
    user_questions = [question.question for question in qa_log.user_questions]
    return user_questions

def get_qa_log_model_answers(db: Session, log_id: int):
    qa_log_info = get_qa_log_info(db, log_id)
    model_answers = [answer.answer for answer in qa_log.model_answers]
    return model_answers

def get_qa_log_model_id(db: Session, log_id: int):
    qa_log_info = get_qa_log_info(db, log_id)
    return qa_log_info.tuned_model_id


############ eval_model_list ############

def get_eval_llm_info(db: Session, llm_eval_name:str):
    eval_llm_info = db.query(models.EvalModelList).filter(models.EvalModelList.llm_eval_name == llm_eval_name).first()
    if eval_llm_info is None:
        raise HTTPException(status_code=404, detail="Input evaluation llm name is not found in DB.")
    return eval_llm_info

def get_eval_llm_api_request_url(db: Session, llm_eval_name: int):
    eval_llm_info = get_eval_llm_info(db, llm_eval_name)
    return eval_llm_info.api_request_url

def get_eval_llm_organization(db: Session, llm_eval_name: int):
    eval_llm_info = get_eval_llm_info(db, llm_eval_name)
    return eval_llm_info.organization

def get_eval_llm_model_version(db: Session, llm_eval_name: int):
    eval_llm_info = get_eval_llm_info(db, llm_eval_name)
    return eval_llm_info.model_version

def get_eval_llm_update_date(db: Session, llm_eval_name: int):
    eval_llm_info = get_eval_llm_info(db, llm_eval_name)
    return eval_llm_info.update_date


############ llm_eval_result ############
def get_llm_eval_result_info(db: Session, eval_id:str):
    eval_result_info = db.query(models.LLMEvalResult).filter(models.LLMEvalResult.eval_id == eval_id).first()
    if eval_result_info is None:
        raise HTTPException(status_code=404, detail="Input llm eval result id is not found in DB.")
    return eval_result_info

############ win_votes ############
# def get_total_votes(db: Session, )