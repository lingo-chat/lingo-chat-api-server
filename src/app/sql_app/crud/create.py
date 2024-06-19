import sys
sys.path.append("../")
from .. import models, schemas

from sqlalchemy.orm import Session

"""
    필요한 CRUD
    그냥 거의 create / read 이다.
    새로운 모델 추가/데이터 추가 / 모델 학습 결과 추가 / 피드백 및 로그 추가...
    
        create all
    
        read
            openmodel list model id
            허 모든 attirbute reading 기능이 있긴 해야하네
        
        update 거의 없음.
            - 기존 open_model_list 에 모델 버전 변경, 업데이트 날짜 변경
            - training dataset url 변경
            - PersonaInfo 업데이트 사항 없음
            - TunedModels 업데이트 사항 없음
            - TrainingArguments wandb link 변경 정도...
            - FeedbackInfo
        
        delete
            - 모델이 삭제되는 경우 정도...

"""


def create_open_model_list(db: Session, open_model_create: schemas.OpenModelListCreate):
    open_model = models.OpenModelList(
        model_id=open_model_create.model_id,
        model_name=open_model_create.model_name,
        size=open_model_create.size,
        base_model_name=open_model_create.base_model_name,
        model_version=open_model_create.model_version,
        update_date=open_model_create.update_date
    )
    db.add(open_model)
    db.commit()
    db.refresh(open_model)
    
    return open_model

def create_train_dataset(db: Session, train_dataset_create: schemas.TrainDatasetCreate):
    train_dataset = models.TrainDataset(
        dataset_name=train_dataset_create.dataset_name,
        categories=train_dataset_create.categories,
        origin=train_dataset_create.origin,
        size=train_dataset_create.size,
        language=train_dataset_create.language,
        domain=train_dataset_create.domain,
        url=train_dataset_create.url
    )
    db.add(train_dataset)
    db.commit()
    db.refresh(train_dataset)
    
    return train_dataset

def create_persona_info(db: Session, persona_info_create: schemas.PersonaInfoCreate):
    persona_info = models.PersonaInfo(
        persona_id=persona_info_create.persona_id,
        persona_name=persona_info_create.persona_name
    )
    db.add(persona_info)
    db.commit()
    db.refresh(persona_info)
    
    return persona_info

def create_tuned_models(db: Session, tuned_models_create: schemas.TunedModelsCreate):
    tuned_model = models.TunedModels(
        tuned_model_id=tuned_models_create.tuned_model_id,
        model_id=tuned_models_create.model_id,
        persona_id=tuned_models_create.persona_id,
        dataset_name=tuned_models_create.dataset_name,
        dataset_categories=tuned_models_create.dataset_categories,
        tuned_model_version=tuned_models_create.tuned_model_version,
        tuned_date=tuned_models_create.tuned_date
    )
    db.add(tuned_model)
    db.commit()
    db.refresh(tuned_model)
    
    return tuned_model

def create_training_arguments(db: Session, training_arguments_create: schemas.TrainingArgumentsCreate):
    training_arguments = models.TrainingArguments(
        tuned_model_id=training_arguments_create.tuned_model_id,
        tuned_categories=training_arguments_create.tuned_categories,
        epoch=training_arguments_create.epoch,
        batch_size=training_arguments_create.batch_size,
        learning_rate=training_arguments_create.learning_rate,
        warmup_steps=training_arguments_create.warmup_steps,
        lr_scheduler=training_arguments_create.lr_scheduler,
        optimizer=training_arguments_create.optimizer,
        wandb_link=training_arguments_create.wandb_link
    )
    db.add(training_arguments)
    db.commit()
    db.refresh(training_arguments)
    
    return training_arguments

def create_feedback_info(db: Session, feedback_info_create: schemas.FeedbackInfoCreate):
    feedback_info = models.FeedbackInfo(
        feedback_id=feedback_info_create.feedback_id,
        tuned_model_id=feedback_info_create.tuned_model_id,
        log_id=feedback_info_create.log_id,
        feedback=feedback_info_create.feedback,
        feedback_time=feedback_info_create.feedback_time
    )
    db.add(feedback_info)
    db.commit()
    db.refresh(feedback_info)
    
    return feedback_info

def create_battle_qa_log(db: Session, 
                         qa_log_create: schemas.QALogCreate, 
                         question_id=None):
    """
        에상 사용법:
            (모델1, 유저 질문 1, 모델 1 답변, 싱글턴 True)
            (모델2, 유저 질문 1, 모델 2 답변, 싱글턴 True) 
            값이 각각 전달(총 2회 전달되는 거임)
            
            먼저 QALog 에 저장하고, 각 질문과 답변을 각각의 테이블에 저장
            질문은 중복되므로, 두 번째 호출 시 질문은 저장하지 않음.
            
            검색 시
                QALog 테이블에서 single_turn=True, tuned_model_id 동일 & question_id 동일 기준으로 조회하여 나온 log_id 를 
                UserQuestion / ModelAnswer 테이블에서 조회

    """
    # single turn 인 경우(battle mode)
    if question_id is None:
        question_id = qa_log_create.question_id
    
    qa_log = models.QALog(
        question_id=question_id,                        # battle mode에서는 같은 질문은 같은 question id
        tuned_model_id=qa_log_create.tuned_model_id,
        is_single_turn=qa_log_create.is_single_turn,    # True
        user_id=qa_log_create.user_id,
        chat_time=qa_log_create.chat_time
    )
    db.add(qa_log)
    db.commit()
    db.refresh(qa_log)

    question_log = db.query(models.UserQuestion).filter(models.UserQuestion.log_id==qa_log.log_id)
    if question_log.first():
        pass
    else:
        question_log = models.UserQuestion(
            log_id=qa_log.log_id,
            question=qa_log_create.question,
        )
        db.add(question_log)
        db.commit()
        db.refresh(question_log)
    
    answer_log = models.ModelAnswer(
        log_id=qa_log.log_id,
        answer=qa_log_create.answer,
        response_gen_time_elapsed=qa_log_create.response_gen_time_elapsed,
    )
    db.add(answer_log)
    db.commit()
    db.refresh(answer_log)
    return qa_log, question_log, answer_log


def create_single_mode_qa_log(db: Session, qa_log_create: schemas.QALogCreate, question_id=None):
    # multi turn 인 경우(single model mode)
    
    """
        검색 시
            QALog 테이블에서 single_turn=False, tuned_model_id 동일 & question_id이 같지않은 기준으로 조회하여 나온 log_id 를 
            UserQuestion / ModelAnswer 테이블에서 조회
            + user_id 같은 경우로만
    """
    qa_log = models.QALog(
        question_id=qa_log_create.question_id,        
        # log_id=qa_log_create.log_id                   # auto incremental
        tuned_model_id=qa_log_create.tuned_model_id,
        is_single_turn=qa_log_create.is_single_turn,    # False
        user_id=qa_log_create.user_id,
        chat_time=qa_log_create.chat_time
    )
    db.add(qa_log)
    db.commit()
    db.refresh(qa_log)
    
    question_log = models.UserQuestion(
        log_id=qa_log.log_id,
        question=qa_log_create.question,
    )
    db.add(question_log)
    db.commit()
    db.refresh(question_log)
    
    answer_log = models.ModelAnswer(
        log_id=qa_log.log_id,
        answer=qa_log_create.answer,
        response_gen_time_elapsed=qa_log_create.response_gen_time_elapsed,
    )
    db.add(answer_log)
    db.commit()
    db.refresh(answer_log)
    
    return qa_log, question_log, answer_log
    
    
    
# def create_user_question(db: Session, user_question_create: schemas.UserQuestionCreate):
#     user_question = models.UserQuestion(
#         log_id=user_question_create.log_id,
#         question=user_question_create.question
#     )
#     db.add(user_question)
#     db.commit()
#     db.refresh(user_question)
    
#     return user_question

# def create_model_answer(db: Session, model_answer_create: schemas.ModelAnswerCreate):
#     model_answer = models.ModelAnswer(
#         log_id=model_answer_create.log_id,
#         answer=model_answer_create.answer,
#         response_gen_time_elapsed=model_answer_create.response_gen_time_elapsed
#     )
#     db.add(model_answer)
#     db.commit()
#     db.refresh(model_answer)
    
#     return model_answer

def create_eval_model_list(db: Session, eval_model_list_create: schemas.EvalModelListCreate):
    eval_model_list = models.EvalModelList(
        llm_eval_name=eval_model_list_create.llm_eval_name,
        api_request_url=eval_model_list_create.api_request_url,
        organization=eval_model_list_create.organization,
        model_version=eval_model_list_create.model_version,
        update_date=eval_model_list_create.update_date
    )
    db.add(eval_model_list)
    db.commit()
    db.refresh(eval_model_list)
    
    return eval_model_list

def create_llm_eval_result(db: Session, llm_eval_result_create: schemas.LLMEvalResultCreate):
    llm_eval_result = models.LLMEvalResult(
        eval_id=llm_eval_result_create.eval_id,
        llm_eval_name=llm_eval_result_create.llm_eval_name,
        tuned_model_id=llm_eval_result_create.tuned_model_id,
        persona_fidelity_score=llm_eval_result_create.persona_fidelity_score,
        friendliness_score=llm_eval_result_create.friendliness_score,
        accuracy_score=llm_eval_result_create.accuracy_score,
        avg_score=llm_eval_result_create.avg_score,
        eval_time=llm_eval_result_create.eval_time
    )
    db.add(llm_eval_result)
    db.commit()
    db.refresh(llm_eval_result)
    
    return llm_eval_result

def create_win_votes(db: Session, win_votes_create: schemas.WinVotesCreate):
    win_votes = models.WinVotes(
        model_a_id=win_votes_create.model_a_id,
        model_b_id=win_votes_create.model_b_id,
        win_model=win_votes_create.win_model,
        vote_date=win_votes_create.vote_date
    )
    db.add(win_votes)
    db.commit()
    db.refresh(win_votes)
    
    return win_votes
