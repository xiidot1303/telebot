<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddLatUzToSettingsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('settings', function (Blueprint $table) {
            $table->text('faq_latuz')->nullable();
            $table->text('about_latuz')->nullable();
            $table->text('partners_latuz')->nullable();
            $table->text('news_latuz')->nullable();
            $table->text('support_latuz')->nullable();
            $table->text('partners_tariffs_latuz')->nullable();
            $table->string('partners_ad_image_latuz')->nullable();
            $table->string('support_image_latuz')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('settings', function (Blueprint $table) {
            $table->dropColumn('faq_latuz');
            $table->dropColumn('about_latuz');
            $table->dropColumn('partners_latuz');
            $table->dropColumn('news_latuz');
            $table->dropColumn('support_latuz');
            $table->dropColumn('partners_tariffs_latuz');
            $table->dropColumn('partners_ad_image_latuz');
            $table->dropColumn('support_image_latuz');
        });
    }
}
