
from fastapi import  HTTPException


def get_recommendations(place_name, df, cosine_sim, top_n=3):
    try:
        place_info = df[df['name'] == place_name].iloc[0]
        place_address = place_info['address']
    except IndexError:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Filter places with the same address
    same_address_df = df[df['address'] == place_address].copy()
    
    if same_address_df.empty:
        raise HTTPException(status_code=404, detail="No places found with the same address")

    idx = same_address_df[same_address_df['name'] == place_name].index[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Get top 'top_n' similar places
    place_indices = [i[0] for i in sim_scores if i[0] in same_address_df.index]
    
    recommendations = same_address_df.loc[place_indices, ['name', 'address']].copy()
    recommendations['index'] = place_indices
    return recommendations