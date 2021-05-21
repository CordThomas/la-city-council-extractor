"""
    Data structure maps the HTML labels to the table field names.
"""
cf_fields = {
    'Council District': 'council_district',
    'Direct to Council': 'direct_to_council',
    'Expiration Date': 'date_expiration',
    'Last Changed Date': 'date_last_changed',
    'Date Received / Introduced': 'date_received',
    'Initiated by': 'initiated_by',
    'Mover': 'mover',
    'Mover/Seconder Comment': 'mover_comment',
    'Pending in Committee': 'pending_committee',
    'Reference Numbers': 'reference_recs',
    'Second': 'second',
    'Title': 'title',
    'Reward Amount': 'reward_amount',
    'Reward Duration': 'reward_duration',
    'Reward Publish Date': 'reward_publish_date',
    'Reward Expire Date': 'reward_expire_date'
}

cf_vote_fields = {
    'Meeting Date:': 'meeting_date',
    'Meeting Type:': 'meeting_type',
    'Vote Action:': 'vote_action'
}

cf_vote_results = {
    'Member Name': 'council_member',
    'CD': 'council_district',
    'Vote': 'vote'
}