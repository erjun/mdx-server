var script = document.createElement("script");
script.src = "_LM5Switch.js";
document.getElementsByTagName('head')[0].appendChild(script);
$('.LDOCE_switch_lang').on('mousedown', function () {
    $(this).find('.cn_txt').addClass('mustShow')
    $(this).next().find('.cn_txt').addClass('mustShow')
})
$('.HWD').on('click', function () {
    let index = $('.HWD').index(this);
    $('.HWD').eq(index + 1)[0].scrollIntoView();
})
jQuery('.LDOCE5pp_sensefold').on('click', function () {
    $(this).parent().find('.ColloExa,.EXAMPLE,.GramExa,.EXAMPLE,.EXAMPLE').toggle()
});