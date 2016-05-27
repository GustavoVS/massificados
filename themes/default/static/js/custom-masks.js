$(document).ready(function(){
  $('input.mask-date, .mask-date input').mask('00/00/0000');
  $('input.mask-time, .mask-time input').mask('00:00:00');
  $('input.mask-date_time, .mask-date_time input').mask('00/00/0000 00:00:00');
  $('input.mask-cep, .mask-cep input').mask('00000-000');
  $('input.mask-phone, .mask-phone input').mask('(00) 0000-0000');
  $('input.mask-cpf, .mask-cpf input').mask('000.000.000-00');
  $('input.mask-cnpj, .mask-cnpj input').mask('00.000.000/0000-00');
  $('input.mask-float, .mask-float input').mask('000.000.000.000.000,00', {reverse: true});
  // $('input.mask-float, .mask-float input').mask("#.##0,00", {reverse: true});
  $('input.mask-percent, .mask-percent input').mask('##0,00%', {reverse: true});
  $('input.mask-number, .mask-number input').mask('##0');
});