<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddReferralLatUzb extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('referral_tenders', function (Blueprint $table) {
            $table->text('latuz_description')->default('');
            $table->string('image_latuz')->nullable();
        });

        Schema::table('referral_tender_levels', function (Blueprint $table) {
            $table->text('latuz_reward')->default('');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('referral_tenders', function (Blueprint $table) {
            $table->dropColumn('latuz_description');
            $table->dropColumn('image_latuz');
        });

        Schema::table('referral_tender_levels', function (Blueprint $table) {
            $table->dropColumn('latuz_reward');
        });
    }
}
