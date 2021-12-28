<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class ReferralTenderLevel extends Model
{
    protected $fillable = [
        'users_from', 'users_to', 'ru_reward', 'uz_reward', 'latuz_reward', 'referral_tender_id'
    ];

    public function referralTender()
    {
        return $this->belongsTo(ReferralTender::class);
    }
}
