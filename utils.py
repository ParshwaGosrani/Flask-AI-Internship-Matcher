import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 'all-mpnet-base-v2' provides the highest quality and accuracy for text matching, 
# offering deeper semantic understanding at the cost of some speed.
model = SentenceTransformer('all-mpnet-base-v2')

def preprocess_data(students_df, employers_df):
    """Cleans data and splits it into Hard Skills vs Soft Interests for weighted AI matching."""
    
    if not students_df.empty and '_id' in students_df.columns:
        students_df['_id'] = students_df['_id'].astype(str)
    if not employers_df.empty and '_id' in employers_df.columns:
        employers_df['_id'] = employers_df['_id'].astype(str)

    # Preprocess Students
    if not students_df.empty:
        students_df.fillna('', inplace=True)
        # Group 1: Hard Skills & Academics
        skills = students_df.get('skills', pd.Series(['']*len(students_df))).astype(str)
        academic = students_df.get('academic_background', pd.Series(['']*len(students_df))).astype(str)
        students_df['hard_skills'] = skills + " " + academic
        
        # Group 2: Soft Interests & Aspirations
        interests = students_df.get('interests', pd.Series(['']*len(students_df))).astype(str)
        aspirations = students_df.get('aspirations', pd.Series(['']*len(students_df))).astype(str)
        students_df['soft_interests'] = interests + " " + aspirations
    else:
        students_df['hard_skills'] = pd.Series(dtype=str)
        students_df['soft_interests'] = pd.Series(dtype=str)

    # Preprocess Employers
    if not employers_df.empty:
        employers_df.fillna('', inplace=True)
        # Group 1: Strict Requirements
        req_skills = employers_df.get('required_skills', pd.Series(['']*len(employers_df))).astype(str)
        employers_df['req_skills'] = req_skills
        
        # Group 2: General Description & Culture
        pos = employers_df.get('position_offered', pd.Series(['']*len(employers_df))).astype(str)
        desc = employers_df.get('description', pd.Series(['']*len(employers_df))).astype(str)
        employers_df['gen_desc'] = pos + " " + desc
    else:
        employers_df['req_skills'] = pd.Series(dtype=str)
        employers_df['gen_desc'] = pd.Series(dtype=str)

    return students_df, employers_df


def create_and_save_embeddings(students_df, employers_df):
    """Generates dual-embeddings (Skills and Interests) for a more accurate matching algorithm."""
    print("Preprocessing data and generating high-accuracy NLP embeddings...")
    stud_df_proc, emp_df_proc = preprocess_data(students_df, employers_df)

    student_embeds = ([], [])
    employer_embeds = ([], [])

    if not stud_df_proc.empty:
        skill_emb = model.encode(stud_df_proc['hard_skills'].tolist())
        int_emb = model.encode(stud_df_proc['soft_interests'].tolist())
        student_embeds = (skill_emb, int_emb) # Packaged as a tuple

    if not emp_df_proc.empty:
        req_emb = model.encode(emp_df_proc['req_skills'].tolist())
        desc_emb = model.encode(emp_df_proc['gen_desc'].tolist())
        employer_embeds = (req_emb, desc_emb) # Packaged as a tuple

    return student_embeds, employer_embeds, stud_df_proc, emp_df_proc


def find_top_matches(student_id, stud_df_proc, emp_df_proc, student_embeds, employer_embeds, top_n=5):
    """Calculates weighted cosine similarity (70% Skills, 30% Culture Fit) for best matches."""
    
    if emp_df_proc.empty or len(employer_embeds[0]) == 0:
        return []

    student_idx_list = stud_df_proc.index[stud_df_proc['_id'] == str(student_id)].tolist()
    if not student_idx_list:
        return []
        
    student_idx = student_idx_list[0]
    
    # Unpack the specific student's vectors
    stu_skill_vec = student_embeds[0][student_idx].reshape(1, -1)
    stu_int_vec = student_embeds[1][student_idx].reshape(1, -1)

    # Unpack all employer vectors
    emp_req_vecs = employer_embeds[0]
    emp_desc_vecs = employer_embeds[1]

    # Calculate two separate semantic similarity scores
    skill_sim = cosine_similarity(stu_skill_vec, emp_req_vecs)[0]
    int_sim = cosine_similarity(stu_int_vec, emp_desc_vecs)[0]

    # THE MAGIC: Blended Weighted Scoring
    # 70% weight on Hard Skills, 30% weight on General Interests/Description
    final_similarities = (skill_sim * 0.70) + (int_sim * 0.30)

    top_indices = np.argsort(final_similarities)[::-1][:top_n]

    matches = []
    for idx in top_indices:
        match_percentage = float(round(max(final_similarities[idx], 0) * 100, 2))
        employer_data = emp_df_proc.iloc[idx]
        
        matches.append({
            'company_name': employer_data.get('company_name', 'Unknown'),
            'position': employer_data.get('position_offered', 'Internship'),
            'location': employer_data.get('location_of_work', 'Remote'),
            'stipend': employer_data.get('stipend', 'Unpaid'),
            'match_percentage': match_percentage,
            'description': str(employer_data.get('description', ''))[:120] + '...',
            'matched_keywords': [] 
        })

    return matches