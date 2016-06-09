# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from partner.models import Partner
from product.models import Status, FileType, InsuranceCompany, Branch, Product, Profile, ActionStatus, MethodPayment, RuleProduct
from sale.models import ActivityArea, NumberLives
from user_account.models import MassificadoUser
from user_groups.models import MassificadoGroups
from status_emails.models import ActionStatusEmails, ActionStatusEmailsUsers


RULES_DEFAULT = (
 ('Morte (Básica)', 100,	3, '', 'V', 0, 'p =  {id_deadline_set-0-payment}; v =  {id_deadline_set-0-lives}; tx=  0.03; ci= (p/12)/(v*tx); if (ci>500000) {value = 50000,00;} else {value = (p/12)/ci);}'),
 ('IEA - Indenização Especial por Acidente', 100,	3, '', 'V', 0, 'p =  {id_deadline_set-0-payment}; v =  {id_deadline_set-0-lives}; tx=  0.03; ci= (p/12)/(v*tx); if (ci>500000) {value = 50000,00;} else {value = (p/12)/ci);}'),
 ('IPA - Invalidez Permanente Total ou Parcial por Acidente', 100,	3, '', 'V', 0, 'p =  {id_deadline_set-0-payment}; v =  {id_deadline_set-0-lives}; tx=  0.03; ci= (p/12)/(v*tx); if (ci>500000) {value = 50000,00;} else {value = (p/12)/ci);}'),
 ('IPD-F - Invalidez Funcional Permanente Total por Doença', 100,	3, '', 'V', 0, 'p =  {id_deadline_set-0-payment}; v =  {id_deadline_set-0-lives}; tx=  0.03; ci= (p/12)/(v*tx); if (ci>500000) {value = 50000,00;} else {value = (p/12)/ci);}'),
 ('Assistência Funeral Individual', 0,	3, 'Serviço', 'F', 3000, 'value = value'),
 ('Morte - Morte Acidetal', 100, 3, '', 'V', 0, 'p =  {id_deadline_set-0-payment}; v =  {id_deadline_set-0-lives}; tx=  0.03; ci= (p/12)/(v*tx); if (ci>500000) {value = 50000,00;} else {value = (p/12)/ci);}'),
)

RULES_VIDA_GLOBAL = ('Morte (Básica)', 'IEA - Indenização Especial por Acidente',
                     'IPA - Invalidez Permanente Total ou Parcial por Acidente',
                     'IPD-F - Invalidez Funcional Permanente Total por Doença',
                     'Assistência Funeral Individual',)

RULES_VIDA = ('Morte (Básica)', 'IEA - Indenização Especial por Acidente',
                     'IPA - Invalidez Permanente Total ou Parcial por Acidente',
                     'IPD-F - Invalidez Funcional Permanente Total por Doença',
                     'Assistência Funeral Individual',)

RULES_AP = (
 'Morte - Morte Acidetal',
 'IPA - Invalidez Permanente Total ou Parcial por Acidente',
)

RULEJS_VIDA_GLOBAL = '''
            function calculate() {
                var P = $('#id_deadline_set-0-payment').val();
                if(P === ""){
                     P =  0;
                }else{
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(",",".");
                     P = parseFloat(P);
                }
                var V = $('#id_deadline_set-0-lives').val();
                if (V===""){V=0}
                if (V === 0 || P === 0) {
                    $('#id_deadline_set-0-insured_capital').val(0).removeClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(0).removeClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(0);
                    $('td.deadline_set-0-rules-valueV').html(0).removeClass("float-success");
                    $('td.deadline_set-0-rules-valueF').removeClass("float-warning");
                }
                else {
                    var CS = (P/(12*V))/0.03;
                    var TXS = (P/(CS))*1000;
                    var CSI = CS;
                    if (CSI>100000 & CS > 0){CSI=100000}

                    if(CSI >0)
                     {
                         $('.table-clauses').removeClass("hidden");
                     }
                    else
                    {
                        $('.table-clauses').addClass("hidden");
                     }

                    CS  = parseFloat(CS).toFixed(2).replace(",",".");
                    TXS = parseFloat(TXS).toFixed(2).replace(",",".");
                    CSI = parseFloat(CSI).toFixed(2).replace(".",",");

                    $('#id_deadline_set-0-insured_capital').val(CS).addClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(TXS).addClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(CSI);
                    $('td.deadline_set-0-rules-valueV').html(CSI).addClass("float-success");
                    $('td.deadline_set-0-rules-valueF').addClass("float-warning");
                }

            }

            $('input#id_deadline_set-0-payment').blur(function(){
                calculate()
            });
            $('input#id_deadline_set-0-payment').keyup(function(){
                calculate()
            });
            $('select#id_deadline_set-0-lives').change(function(){
                calculate()
            });
'''

RULEJS_VIDA = '''
            function calculate() {
                var P = $('#id_deadline_set-0-payment').val();
                if(P === ""){
                     P =  0;
                }else{
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(",",".");
                     P = parseFloat(P);
                }
                var V = $('#id_deadline_set-0-lives').val();
                if (V===""){V=0}
                if (V === 0 || P === 0) {
                    $('#id_deadline_set-0-insured_capital').val(0).removeClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(0).removeClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(0);
                    $('td.deadline_set-0-rules-valueV').html(0).removeClass("float-success");
                    $('td.deadline_set-0-rules-valueF').removeClass("float-warning");
                }
                else {
                    var CS = (P/(12*V))/0.03;
                    if (CS>100000){CS=100000}
                    var CSI = CS;
                    CS=CS*V;
                    var TXS = (P/(CS))*1000;
                    if(CSI >0)
                     {
                         $('.table-clauses').removeClass("hidden");
                     }
                    else
                    {
                        $('.table-clauses').addClass("hidden");
                     }

                    CS  = parseFloat(CS).toFixed(2).replace(",",".");
                    TXS = parseFloat(TXS).toFixed(2).replace(",",".");
                    CSI = parseFloat(CSI).toFixed(2).replace(".",",");

                    $('#id_deadline_set-0-insured_capital').val(CS).addClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(TXS).addClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(CSI);
                    $('td.deadline_set-0-rules-valueV').html(CSI).addClass("float-success");
                    $('td.deadline_set-0-rules-valueF').addClass("float-warning");
                }

            }

            $('input#id_deadline_set-0-payment').blur(function(){
                calculate()
            });
            $('input#id_deadline_set-0-payment').keyup(function(){
                calculate()
            });
            $('select#id_deadline_set-0-lives').change(function(){
                calculate()
            });
'''

RULEJS_AP = '''
            function calculate() {
                var P = $('#id_deadline_set-0-payment').val();
                if(P === ""){
                     P =  0;
                }else{
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(".","");
                     P = P.replace(",",".");
                     P = parseFloat(P);
                }
                var V = $('#id_deadline_set-0-lives').val();
                if (V===""){V=0}
                if (V === 0 || P === 0) {
                    $('#id_deadline_set-0-insured_capital').val(0).removeClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(0).removeClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(0);
                    $('td.deadline_set-0-rules-valueV').html(0).removeClass("float-success");
                    $('td.deadline_set-0-rules-valueF').removeClass("float-warning");
                }
                else {
                    var CS = (P/(12*V))/0.03;
                    if (CS>100000){CS=100000}
                    var CSI = CS;
                    CS=CS*V;
                    var TXS = (P/(CS))*1000;

                    if(CSI >0)
                     {
                         $('.table-clauses').removeClass("hidden");
                     }
                    else
                    {
                        $('.table-clauses').addClass("hidden");
                     }

                    CS  = parseFloat(CS).toFixed(2).replace(",",".");
                    TXS = parseFloat(TXS).toFixed(2).replace(",",".");
                    CSI = parseFloat(CSI).toFixed(2).replace(".",",");

                    $('#id_deadline_set-0-insured_capital').val(CS).addClass("float-success");
                    $('#id_deadline_set-0-rate_per_thousand').val(TXS).addClass("float-success");

                    $('input.deadline_set-0-rules-valueV').val(CSI);
                    $('td.deadline_set-0-rules-valueV').html(CSI).addClass("float-success");
                    $('td.deadline_set-0-rules-valueF').addClass("float-warning");
                }

            }

            $('input#id_deadline_set-0-payment').blur(function(){
                calculate()
            });
            $('input#id_deadline_set-0-payment').keyup(function(){
                calculate()
            });
            $('select#id_deadline_set-0-lives').change(function(){
                calculate()
            });
'''


FULL_DECLARATION_VIDA = '''<h1><strong>CONDI&Ccedil;&Otilde;ES RESUMIDAS DO PLANO</strong></h1>
<h2><strong>Coberturas</strong></h2>
<p><strong>CB - Cobertura B&aacute;sica (Morte) - garante aos benifici&aacute;rios o pagamento do capital segurado individual contratado para esta cobertura, em caso de morte do segurado, seja natural, seja acidental, devidamente coberta, exceto se decorrente de riscos exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>IEA - Indeniza&ccedil;&atilde;o Especial por Acidente - garante aos benefici&aacute;rios o pagamento do capital segurado individual contratado para esta cobertura em caso de morte do segurado causada, exclusivamente, por acidente pessoal coberto pelo seguro, exceto se decorrente de riscos excluidos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong><strong><br /></strong></p>
<p><strong>IPA - Invalidez Permanente Total ou Parcial por Acidente - garante ao pr&oacute;prio segurado o pagamento do capital segurado individual contratado proporcional &agrave; perda ou redu&ccedil;&atilde;o funcional de um membro ou &oacute;rg&atilde;o, sofrida em consequencia de acidente pessoal coberto, exceto se decorrente de riscos exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro. O valor correspondente at&eacute; 100% (cem por cento) do capital da cobertura B&aacute;sica. Para c&aacute;lculo do capital segurado a ser pago ser&aacute; utilizado a tabela de c&aacute;lculo para Invalidez Parcial que faz parte das Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>&nbsp;IPD-F - Invalidez Funcional Permanente Total por Doen&ccedil;a - garante ao pr&oacute;prio Segurado o pagamento antecipado do Capital Segurado Individual contratado para a cobertura b&aacute;sica (morte), em caso de sua invalidez funcional permanente total por doen&ccedil;a, exceto se decorrente dos risco exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p>A aposentadoria por invalidez concedida por institui&ccedil;&otilde;es oficiais de previd&ecirc;ncia social, assim como por &Oacute;rg&atilde;os do Poder P&uacute;blico e por outras institui&ccedil;&otilde;es P&uacute;blico-Privadas, n&atilde;o caracteriza, por si s&oacute;, Quadro Cl&iacute;nico Incapacitante que comprove a Invalidez Funcional Permanente e Total por Doen&ccedil;a.</p>
<p>A cobertura de Invalidez Funcional Permanente Total por Doen&ccedil;a n&atilde;o se acumula com as demais coberturas contratadas neste seguro.</p>
<h2><strong>Servi&ccedil;o de Assist&ecirc;ncia Funeral "Titular"</strong></h2>
<p>O Servi&ccedil;o de Assist&ecirc;ncia Funeral tem por objetivo propiciar aos benefici&aacute;rios em caso de falecimento do segurado Titular todo aux&iacute;lio e presta&ccedil;&atilde;o de servi&ccedil;os relativos ao funeral, disponibilizando um representante oficial da Seguradora que tomar&aacute; todas as provid&ecirc;ncias necess&aacute;rias para a realiza&ccedil;&atilde;o do mesmo.</p>
<p>O conjunto dos servi&ccedil;os e itens garantidos pelo seguro estar&aacute; limitado ao valor m&aacute;ximo de despesas equivalente a R$ 3.000,00 (tr&ecirc;s mil reais).</p>
<p>No caso da n&atilde;o utiliza&ccedil;&atilde;o dos servi&ccedil;os ser&aacute; reembolsado, mediante a apresenta&ccedil;&atilde;o de notas fiscais originais, o valor m&aacute;ximo de R$ 3.000,00 (tr&ecirc;s mil reais) referente aos gastos com os servi&ccedil;os garantidos.</p>
<p>Os Servi&ccedil;os a seguir especificados ser&atilde;o prestados exclusivamente mediante o acionamento da Central de Atendimento de Servi&ccedil;os Assistenciais (Brasil: 0800 707 5050 &ndash; Exterior: 5511 4689 5628) pelos Familiares, Benefici&aacute;rios ou o Representante do Estipulante,</p>
<p>O Servi&ccedil;o de Assist&ecirc;ncia Funeral garante, de acordo com o limite de despesa estabelecida acima, a presta&ccedil;&atilde;o dos servi&ccedil;os de sepultamento ou crema&ccedil;&atilde;o (onde existir esse servi&ccedil;o) que englobem os seguintes itens:</p>
<p>Urna;</p>
<p>Carro para enterro (no munic&iacute;pio de moradia habitual do Segurado);</p>
<p>Carreto / caix&atilde;o (no munic&iacute;pio de moradia habitual do Segurado);</p>
<p>Servi&ccedil;o Assistencial;</p>
<p>Registro de &oacute;bito;</p>
<p>Taxa de sepultamento ou crema&ccedil;&atilde;o;</p>
<p>Remo&ccedil;&atilde;o do corpo (no munic&iacute;pio de moradia habitual);</p>
<p>Paramentos;</p>
<p>Aparelho de Ozona;</p>
<p>Mesa de Condol&ecirc;ncias;</p>
<p>Velas;</p>
<p>Vel&oacute;rio;</p>
<p>V&eacute;u;</p>
<p>Enfeite Floral e Coroas; e</p>
<p>Loca&ccedil;&atilde;o de jazigo.</p>
<p><strong>Caso a segurado n&atilde;o possua jazigo ou sepultura, a Tokio Marine Seguradora S/A garantir&aacute; a seu crit&eacute;rio e de acordo com o plano contratado, cemit&eacute;rio e jazigo por um per&iacute;odo de at&eacute; 03 (Tr&ecirc;s) anos, tempo necess&aacute;rio para exuma&ccedil;&atilde;o. N&atilde;o sendo poss&iacute;vel sepultamento por motivos alheios &agrave; vontade da Seguradora na cidade indicada pela fam&iacute;lia, este ser&aacute; feito na cidade mais pr&oacute;xima.</strong></p>
<h2><strong>Capitais Segurados</strong></h2>
<p>O Capital Segurado do grupo ser&aacute; uniforme.</p>
<h2><strong>Vig&ecirc;ncia do Seguro</strong></h2>
<p>A ap&oacute;lice viger&aacute; pelo prazo de 12 (doze) meses, a contar da data de in&iacute;cio de vig&ecirc;ncia determinada pelo Estipulante, quando da aprova&ccedil;&atilde;o do seguro e assinatura da Proposta de Contrata&ccedil;&atilde;o, sendo admiss&iacute;vel uma &uacute;nica renova&ccedil;&atilde;o autom&aacute;tica, por igual per&iacute;odo, salvo se o Estipulante ou a Seguradora manifestar-se em sentido contr&aacute;rio, mediante aviso pr&eacute;vio, por escrito, com anteced&ecirc;ncia m&iacute;nima de 60 (sessenta) dias.</p>
<p>Ao t&eacute;rmino do contrato, a ap&oacute;lice poder&aacute; ser renovada mediante confirma&ccedil;&atilde;o por escrito, por mais um per&iacute;odo e assim sucessivamente.</p>
<p>No caso de n&atilde;o renova&ccedil;&atilde;o da ap&oacute;lice mestra, a cobertura de cada segurado cessa automaticamente no final de vig&ecirc;ncia da ap&oacute;lice, respeitando o per&iacute;odo correspondente ao pr&ecirc;mio pago.</p>
<p>Este seguro &eacute; por prazo determinado, tendo a Seguradora a faculdade de n&atilde;o renovar a ap&oacute;lice na data de vencimento, sem devolu&ccedil;&atilde;o dos pr&ecirc;mios pagos nos termos da ap&oacute;lice.</p>
<h2><strong>Condi&ccedil;&otilde;es de Aceita&ccedil;&atilde;o</strong></h2>
<p>Estar&atilde;o incluidos no seguro, todos os funcion&aacute;rios do Estipulante e/ou S&oacute;cios/Diretores, desde que:</p>
<p>a.) estejam em plena atividade profissional/laborativa;</p>
<p>b.) em boas condi&ccedil;&otilde;es de sa&uacute;de;</p>
<p>c.) tenham idade compreendida entre 14 a 65 anos.</p>
<p>Aposentados por Tempo de Servi&ccedil;o e Idade poder&atilde;o participar do seguro desde que estejam em plena atividade de trabalho e constem da Guia de Recolhimento do Fundo de Garantia - GFIP.</p>
<p>Aposentados por Invalidez n&atilde;o poder&atilde;o participar do seguro.</p>
<p>Este seguro n&atilde;o contempla a inclus&atilde;o dos Funcion&aacute;rios e/ou S&oacute;cios/Diretores que estejam afastados de suas atividades laborativas.</p>
<p>O(s) funcion&aacute;rio(s) afastado(s) por doen&ccedil;a ou acidente, antes do in&iacute;cio de vig&ecirc;ncia da ap&oacute;lice, somente ter&aacute;(&atilde;o) direito &agrave; cobertura a partir da data de seu retorno &agrave;s atividades normais de trabalho.</p>
<p><strong>* As Condi&ccedil;&otilde;es Gerais se encontram em poder do Corretora, solicite-as.</strong></p>'''

DECLARATION_VIDA = '''<h1>DECLARA&Ccedil;&Atilde;O E AUTORIZA&Ccedil;&Atilde;O DE DESCONTO</h1>
<p>A empresa acima qualificada como Estipulante da ap&oacute;lice prop&otilde;e a Tokio Marine Seguradora S/A a inclus&atilde;o de seus empregados e/ou S&oacute;cios/Diretores no seguro, conforme rela&ccedil;&atilde;o fornecida e observadas as Condi&ccedil;&otilde;es Contratuais e Condi&ccedil;&otilde;es Gerais do Plano de Seguro de Pessoas - Vida em Grupo - taxa m&eacute;dia.</p>
<p>Declara que recebeu, tomou ci&ecirc;ncia das Condi&ccedil;&otilde;es Contratuais deste Seguro e efetuou o pagamento do pr&ecirc;mio do seguro atrav&eacute;s de quita&ccedil;&atilde;o do boleto referenciado junto a rede banc&aacute;ria.</p>
<p>A empresa concorda que s&oacute; ter&atilde;o cobertura os segurados que ao ingressarem no seguro estiverem em plena atividade de trabalho, n&atilde;o tenham idade superior a 65 anos e estejam em perfeitas condi&ccedil;&otilde;es de sa&uacute;de, n&atilde;o apresentando doen&ccedil;as preexistentes ou sequelas delas provenientes, que impe&ccedil;am seu ingresso no seguro ou que agravem a taxa do pr&ecirc;mio, assumindo integralmente a responsabilidade pelas informa&ccedil;&otilde;es prestadas, ciente e de acordo com os artigos 765 e 766 do C&oacute;digo Civil Brasileiro, se tiver omitido circunst&acirc;ncias que possam influir na aceita&ccedil;&atilde;o ou validade da proposta, no valor do capital ou taxa do pr&ecirc;mio, perder&aacute; o direito ao capital segurado e consequentemente a quaisquer garantias ou pagamentos de benef&iacute;cios.</p>
<p>A aceita&ccedil;&atilde;o do seguro estar&aacute; sujeita a analise do risco.</p>
<p>O registro deste plano na SUSEP n&atilde;o implica, por parte da Autarquia, incentivo ou recomenda&ccedil;&atilde;o a sua comercializa&ccedil;&atilde;o</p>
<p>O segurado poder&aacute; consultar a situa&ccedil;&atilde;o cadastral de seu corretor, no site <a href="http://www.susep.gov.br" target="_blank" >www.susep.gov.br</a>, por meio do n&uacute;mero de registro na SUSEP, nome completo, CNPJ ou CPF.</p>'''

FULL_DECLARATION_VIDA_GLOGAL= '''<h1>CONDI&Ccedil;&Otilde;ES RESUMIDAS DO PLANO</h1>
<h2><strong>Coberturas</strong></h2>
<p><strong>CB - Cobertura B&aacute;sica (Morte) - garante aos benifici&aacute;rios o pagamento do capital segurado individual contratado para esta cobertura, em caso de morte do segurado, seja natural, seja acidental, devidamente coberta, exceto se decorrente de riscos exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>IEA - Indeniza&ccedil;&atilde;o Especial por Acidente - garante aos benefici&aacute;rios o pagamento do capital segurado individual contratado para esta cobertura em caso de morte do segurado causada, exclusivamente, por acidente pessoal coberto pelo seguro, exceto se decorrente de riscos excluidos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>IPA - Invalidez Permanente Total ou Parcial por Acidente - garante ao pr&oacute;prio segurado o pagamento do capital segurado individual contratado proporcional &agrave; perda ou redu&ccedil;&atilde;o funcional de um membro ou &oacute;rg&atilde;o, sofrida em consequencia de acidente pessoal coberto, exceto se decorrente de riscos exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro. O valor correspondente at&eacute; 100% (cem por cento) do capital da cobertura B&aacute;sica. Para c&aacute;lculo do capital segurado a ser pago ser&aacute; utilizado a tabela de c&aacute;lculo para Invalidez Parcial que faz parte das Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>IPD-F - Invalidez Funcional Permanente Total por Doen&ccedil;a - garante ao pr&oacute;prio Segurado o pagamento antecipado do Capital Segurado Individual contratado para a cobertura b&aacute;sica (morte), em caso de sua invalidez funcional permanente total por doen&ccedil;a, exceto se decorrente dos risco exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p>A aposentadoria por invalidez concedida por institui&ccedil;&otilde;es oficiais de previd&ecirc;ncia social, assim como por &Oacute;rg&atilde;os do Poder P&uacute;blico e por outras institui&ccedil;&otilde;es P&uacute;blico-Privadas, n&atilde;o caracteriza, por si s&oacute;, Quadro Cl&iacute;nico Incapacitante que comprove a Invalidez Funcional Permanente e Total por Doen&ccedil;a.</p>
<p>A cobertura de Invalidez Funcional Permanente Total por Doen&ccedil;a n&atilde;o se acumula com as demais coberturas contratadas neste seguro.</p>
<h2><strong>Servi&ccedil;o de Assist&ecirc;ncia Funeral "Titular"</strong></h2>
<p>O Servi&ccedil;o de Assist&ecirc;ncia Funeral tem por objetivo propiciar aos benefici&aacute;rios em caso de falecimento do segurado Titular todo aux&iacute;lio e presta&ccedil;&atilde;o de servi&ccedil;os relativos ao funeral, disponibilizando um representante oficial da Seguradora que tomar&aacute; todas as provid&ecirc;ncias necess&aacute;rias para a realiza&ccedil;&atilde;o do mesmo.</p>
<p>O conjunto dos servi&ccedil;os e itens garantidos pelo seguro estar&aacute; limitado ao valor m&aacute;ximo de despesas equivalente a R$ 3.000,00 (tr&ecirc;s mil reais).</p>
<p>No caso da n&atilde;o utiliza&ccedil;&atilde;o dos servi&ccedil;os ser&aacute; reembolsado, mediante a apresenta&ccedil;&atilde;o de notas fiscais originais, o valor m&aacute;ximo de R$ 3.000,00 (tr&ecirc;s mil reais) referente aos gastos com os servi&ccedil;os garantidos.</p>
<p>Os Servi&ccedil;os a seguir especificados ser&atilde;o prestados exclusivamente mediante o acionamento da Central de Atendimento de Servi&ccedil;os Assistenciais (Brasil: 0800 707 5050 &ndash; Exterior: 5511 4689 5628) pelos Familiares, Benefici&aacute;rios ou o Representante do Estipulante,</p>
<p>O Servi&ccedil;o de Assist&ecirc;ncia Funeral garante, de acordo com o limite de despesa estabelecida acima, a presta&ccedil;&atilde;o dos servi&ccedil;os de sepultamento ou crema&ccedil;&atilde;o (onde existir esse servi&ccedil;o) que englobem os seguintes itens:</p>
<p>Urna;</p>
<p>Carro para enterro (no munic&iacute;pio de moradia habitual do Segurado);</p>
<p>Carreto / caix&atilde;o (no munic&iacute;pio de moradia habitual do Segurado);</p>
<p>Servi&ccedil;o Assistencial;</p>
<p>Registro de &oacute;bito;</p>
<p>Taxa de sepultamento ou crema&ccedil;&atilde;o;</p>
<p>Remo&ccedil;&atilde;o do corpo (no munic&iacute;pio de moradia habitual);</p>
<p>Paramentos;</p>
<p>Aparelho de Ozona;</p>
<p>Mesa de Condol&ecirc;ncias;</p>
<p>Velas;</p>
<p>Vel&oacute;rio;</p>
<p>V&eacute;u;</p>
<p>Enfeite Floral e Coroas; e</p>
<p>Loca&ccedil;&atilde;o de jazigo.</p>
<p><strong>Caso a segurado n&atilde;o possua jazigo ou sepultura, a Tokio Marine Seguradora S/A garantir&aacute; a seu crit&eacute;rio e de acordo com o plano contratado, cemit&eacute;rio e jazigo por um per&iacute;odo de at&eacute; 03 (Tr&ecirc;s) anos, tempo necess&aacute;rio para exuma&ccedil;&atilde;o. N&atilde;o sendo poss&iacute;vel sepultamento por motivos alheios &agrave; vontade da Seguradora na cidade indicada pela fam&iacute;lia, este ser&aacute; feito na cidade mais pr&oacute;xima.</strong></p>
<h2><strong>Capitais Segurados</strong></h2>
<p>O Capital Segurado do grupo ser&aacute; uniforme para todos os funcion&aacute;rios que constarem na GFIP - Guia de Recolhimento de Fundo de Garantia, e para todos os S&oacute;cios/Diretores que constarem do Contrato Social da empresa.</p>
<p>O Capital Segurado Individual ser&aacute; calculado atrav&eacute;s de rateio do Capital Segurado Global Contratado pelo Estipulante para o grupo de Funcion&aacute;rios/S&oacute;cios, pela quantidade de funcion&aacute;rios que constarem na GFIP e S&oacute;cios que constarem do Contrato Social da empresa, respeitando-se o limite m&aacute;ximo estabelecido na Proposta de Contrata&ccedil;&atilde;o.</p>
<p>Se a quantidade de funcion&aacute;rios e/ou s&oacute;cios/diretores se alterar durante a vig&ecirc;ncia do seguro, seja pela ocorr&ecirc;ncia de sinistro ou pela movimenta&ccedil;&atilde;o de funcion&aacute;rios, o Capital Segurado Individual ser&aacute; automaticamente ajustado rateando-se o Capital Total Contratado de forma proporcional ao novo n&uacute;mero de Funcion&aacute;rios e Dirigentes, respeitando-se o limita m&aacute;ximo de Capital Individual estabelecido na Proposta de Contrata&ccedil;&atilde;o.</p>
<h2><strong>Vig&ecirc;ncia do Seguro</strong></h2>
<p>A ap&oacute;lice viger&aacute; pelo prazo de 12 (doze) meses, a contar da data de in&iacute;cio de vig&ecirc;ncia determinada pelo Estipulante, quando da aprova&ccedil;&atilde;o do seguro e assinatura da Proposta de Contrata&ccedil;&atilde;o, sendo admiss&iacute;vel uma &uacute;nica renova&ccedil;&atilde;o autom&aacute;tica, por igual per&iacute;odo, salvo se o Estipulante ou a Seguradora manifestar-se em sentido contr&aacute;rio, mediante aviso pr&eacute;vio, por escrito, com anteced&ecirc;ncia m&iacute;nima de 60 (sessenta) dias.</p>
<p>Ao t&eacute;rmino do contrato, a ap&oacute;lice poder&aacute; ser renovada mediante confirma&ccedil;&atilde;o por escrito, por mais um per&iacute;odo e assim sucessivamente.</p>
<p>No caso de n&atilde;o renova&ccedil;&atilde;o da ap&oacute;lice mestra, a cobertura de cada segurado cessa automaticamente no final de vig&ecirc;ncia da ap&oacute;lice, respeitando o per&iacute;odo correspondente ao pr&ecirc;mio pago.</p>
<p>Este seguro &eacute; por prazo determinado, tendo a Seguradora a faculdade de n&atilde;o renovar a ap&oacute;lice na data de vencimento, sem devolu&ccedil;&atilde;o dos pr&ecirc;mios pagos nos termos da ap&oacute;lice.</p>
<h2><strong>Condi&ccedil;&otilde;es de Aceita&ccedil;&atilde;o</strong></h2>
<p>Estar&atilde;o incluidos no seguro, todos os funcion&aacute;rios do Estipulante que constem da GFIP - Guia de Recolhimento do Fundo de Garantia e Tempo de Servi&ccedil;o e Informa&ccedil;&otilde;es da Previd&ecirc;ncia Social e respectivos S&oacute;cios e/ou Diretores constantes do contrato social, desde que:</p>
<p>a.) estejam em plena atividade profissional/laborativa;</p>
<p>b.) em boas condi&ccedil;&otilde;es de sa&uacute;de;</p>
<p>c.) tenham idade compreendida entre 14 a 65 anos.</p>
<p>Aposentados por Tempo de Servi&ccedil;o e Idade poder&atilde;o participar do seguro desde que estejam em plena atividade de trabalho e constem da Guia de Recolhimento do Fundo de Garantia - GFIP.</p>
<p>Aposentados por Invalidez n&atilde;o poder&atilde;o participar do seguro.</p>
<p>Este seguro n&atilde;o contempla a inclus&atilde;o dos Funcion&aacute;rios e/ou S&oacute;cios/Diretores que estejam afastados de suas atividades laborativas.</p>
<p>O(s) funcion&aacute;rio(s) afastado(s) por doen&ccedil;a ou acidente, antes do in&iacute;cio de vig&ecirc;ncia da ap&oacute;lice, somente ter&aacute;(&atilde;o) direito &agrave; cobertura a partir da data de seu retorno &agrave;s atividades normais de trabalho.</p>
<p><strong>* As Condi&ccedil;&otilde;es Gerais se encontram em poder do Corretora, solicite-as.</strong></p>
'''

DECLARATION_VIDA_GLOGAL = '''<h1>DECLARA&Ccedil;&Atilde;O E AUTORIZA&Ccedil;&Atilde;O DE DESCONTO</h1>
<p>A empresa acima qualificada como Estipulante da ap&oacute;lice prop&otilde;e a Tokio Marine Seguradora S/A a inclus&atilde;o de todos os seus empregados que constem da GFIP - Guia de Recolhimento do Fundo de Garantia e Tempo de Servi&ccedil;o e Informa&ccedil;&otilde;es da Previd&ecirc;ncia Social e respectivos S&oacute;cios e/ou Diretores constantes do Contrato Social, observadas as Condi&ccedil;&otilde;es Contratuais no Plano de Seguro de Pessoas - Capital Global.</p>
<p>Declara que recebeu, tomou ci&ecirc;ncia das Condi&ccedil;&otilde;es Contratuais deste Seguro e efetuou o pagamento do pr&ecirc;mio do seguro atrav&eacute;s de quita&ccedil;&atilde;o do boleto referenciado junto a rede banc&aacute;ria.</p>
<p>A empresa concorda que s&oacute; ter&atilde;o cobertura os segurados que ao ingressarem no seguro estiverem em plena atividade de trabalho, n&atilde;o tenham idade superior ao estabelecido e estejam em perfeitas condi&ccedil;&otilde;es de sa&uacute;de, n&atilde;o apresentando doen&ccedil;as preexistentes ou sequelas delas provenientes, que impe&ccedil;am seu ingresso no seguro ou que agravem a taxa do pr&ecirc;mio, assumindo integralmente a responsabilidade pelas informa&ccedil;&otilde;es prestadas, ciente e de acordo com os artigos 765 e 766 do C&oacute;digo Civil Brasileiro, se tiver omitido circunst&acirc;ncias que possam influir na aceita&ccedil;&atilde;o ou validade da proposta, no valor do capital ou taxa do pr&ecirc;mio, perder&aacute; o direito ao capital segurado e consequentemente a quaisquer garantias ou pagamentos de benef&iacute;cios.</p>
<p>A aceita&ccedil;&atilde;o do seguro estar&aacute; sujeita a analise do risco.</p>
<p>O registro deste plano na SUSEP n&atilde;o implica, por parte da Autarquia, incentivo ou recomenda&ccedil;&atilde;o a sua comercializa&ccedil;&atilde;o</p>
<p>O segurado poder&aacute; consultar a situa&ccedil;&atilde;o cadastral de seu corretor, no site <a href="http://www.susep.gov.br" target="_blank" >www.susep.gov.br</a>, por meio do n&uacute;mero de registro na SUSEP, nome completo, CNPJ ou CPF.</p>'''

FULL_DECLARATION_AP = '''<h1>CONDI&Ccedil;&Otilde;ES RESUMIDAS DO PLANO</h1>
<h2><strong>Coberturas</strong></h2>
<p><strong>MA - Morte Acidental - garante aos benefici&aacute;rios o pagamento do capital segurado individual contratado para esta cobertura em caso de morte do segurado causada, exclusivamente, por acidente pessoal coberto pelo seguro, exceto se decorrente de riscos excluidos, conforme Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<p><strong>IPA - Invalidez Permanente Total ou Parcial por Acidente - garante ao pr&oacute;prio segurado o pagamento do capital segurado individual contratado proporcional &agrave; perda ou redu&ccedil;&atilde;o funcional de um membro ou &oacute;rg&atilde;o, sofrida em consequencia de acidente pessoal coberto, exceto se decorrente de riscos exclu&iacute;dos, conforme Condi&ccedil;&otilde;es Gerais do Seguro. O valor correspondente at&eacute; 100% (cem por cento) do capital da cobertura B&aacute;sica. Para c&aacute;lculo do capital segurado a ser pago ser&aacute; utilizado a tabela de c&aacute;lculo para Invalidez Parcial que faz parte das Condi&ccedil;&otilde;es Gerais do Seguro.</strong></p>
<h2>Capitais Segurados</h2>
<p>O Capital Segurado do grupo ser&aacute; uniforme.</p>
<p><strong>Vig&ecirc;ncia do Seguro</strong></p>
<p>A ap&oacute;lice viger&aacute; pelo prazo de 12 (doze) meses, a contar da data de in&iacute;cio de vig&ecirc;ncia determinada pelo Estipulante, quando da aprova&ccedil;&atilde;o do seguro e assinatura da Proposta de Contrata&ccedil;&atilde;o, sendo admiss&iacute;vel uma &uacute;nica renova&ccedil;&atilde;o autom&aacute;tica, por igual per&iacute;odo, salvo se o Estipulante ou a Seguradora manifestar-se em sentido contr&aacute;rio, mediante aviso pr&eacute;vio, por escrito, com anteced&ecirc;ncia m&iacute;nima de 60 (sessenta) dias.</p>
<p>Ao t&eacute;rmino do contrato, a ap&oacute;lice poder&aacute; ser renovada mediante confirma&ccedil;&atilde;o por escrito, por mais um per&iacute;odo e assim sucessivamente.</p>
<p>No caso de n&atilde;o renova&ccedil;&atilde;o da ap&oacute;lice mestra, a cobertura de cada segurado cessa automaticamente no final de vig&ecirc;ncia da ap&oacute;lice, respeitando o per&iacute;odo correspondente ao pr&ecirc;mio pago.</p>
<p>Este seguro &eacute; por prazo determinado, tendo a Seguradora a faculdade de n&atilde;o renovar a ap&oacute;lice na data de vencimento, sem devolu&ccedil;&atilde;o dos pr&ecirc;mios pagos nos termos da ap&oacute;lice.</p>
<h2>Condi&ccedil;&otilde;es de Aceita&ccedil;&atilde;o</h2>
<p>Estar&atilde;o incluidos no seguro, todos os funcion&aacute;rios do Estipulante e/ou S&oacute;cios/Diretores, desde que:</p>
<p>a.) estejam em plena atividade profissional/laborativa;</p>
<p>b.) em boas condi&ccedil;&otilde;es de sa&uacute;de;</p>
<p>c.) tenham idade compreendida entre 14 a 70 anos.</p>
<p>Aposentados por Tempo de Servi&ccedil;o e Idade poder&atilde;o participar do seguro desde que estejam em plena atividade de trabalho e constem da Guia de Recolhimento do Fundo de Garantia - GFIP.</p>
<p>Aposentados por Invalidez n&atilde;o poder&atilde;o participar do seguro.</p>
<p>Este seguro n&atilde;o contempla a inclus&atilde;o dos Funcion&aacute;rios e/ou S&oacute;cios/Diretores que estejam afastados de suas atividades laborativas.</p>
<p>O(s) funcion&aacute;rio(s) afastado(s) por doen&ccedil;a ou acidente, antes do in&iacute;cio de vig&ecirc;ncia da ap&oacute;lice, somente ter&aacute;(&atilde;o) direito &agrave; cobertura a partir da data de seu retorno &agrave;s atividades normais de trabalho.</p>
<p><strong>* As Condi&ccedil;&otilde;es Gerais se encontram em poder do Corretora, solicite-as.</strong></p>'''

DECLARATION_AP = '''<h1>DECLARA&Ccedil;&Atilde;O E AUTORIZA&Ccedil;&Atilde;O DE DESCONTO</h1>
<p>A empresa acima qualificada como Estipulante da ap&oacute;lice prop&otilde;e a Tokio Marine Seguradora S/A a inclus&atilde;o de seus empregados e/ou S&oacute;cios/Diretores no seguro, conforme rela&ccedil;&atilde;o fornecida e observadas as Condi&ccedil;&otilde;es Contratuais e Condi&ccedil;&otilde;es Gerais do Plano de Seguro de Pessoas - Acidentes Pessoais Coletivo.</p>
<p>Declara que recebeu, tomou ci&ecirc;ncia das Condi&ccedil;&otilde;es Contratuais deste Seguro e efetuou o pagamento do pr&ecirc;mio do seguro atrav&eacute;s de quita&ccedil;&atilde;o do boleto referenciado junto a rede banc&aacute;ria.</p>
<p>A empresa concorda que s&oacute; ter&atilde;o cobertura os segurados que ao ingressarem no seguro estiverem em plena atividade de trabalho, n&atilde;o tenham idade superior ao estabelecido e estejam em perfeitas condi&ccedil;&otilde;es de sa&uacute;de, n&atilde;o apresentando doen&ccedil;as preexistentes ou sequelas delas provenientes, que impe&ccedil;am seu ingresso no seguro ou que agravem a taxa do pr&ecirc;mio, assumindo integralmente a responsabilidade pelas informa&ccedil;&otilde;es prestadas, ciente e de acordo com os artigos 765 e 766 do C&oacute;digo Civil Brasileiro, se tiver omitido circunst&acirc;ncias que possam influir na aceita&ccedil;&atilde;o ou validade da proposta, no valor do capital ou taxa do pr&ecirc;mio, perder&aacute; o direito ao capital segurado e consequentemente a quaisquer garantias ou pagamentos de benef&iacute;cios.</p>
<p>A aceita&ccedil;&atilde;o do seguro estar&aacute; sujeita a analise do risco.</p>
<p>O registro deste plano na SUSEP n&atilde;o implica, por parte da Autarquia, incentivo ou recomenda&ccedil;&atilde;o a sua comercializa&ccedil;&atilde;o</p>
<p>O segurado poder&aacute; consultar a situa&ccedil;&atilde;o cadastral de seu corretor, no site <a href="http://www.susep.gov.br" target="_blank" >www.susep.gov.br</a>, por meio do n&uacute;mero de registro na SUSEP, nome completo, CNPJ ou CPF.</p>'''

AREA = ("Academia de Esportes / Artes Marciais",
"Açúcar e Álcool",
"Administração e Participação",
"Agências de Turismo / Viagem",
"Agricultura / Pecuária / Silvicultura",
"Alimentos",
"Arquitetura / Paisagismo / Urbanismo",
"Assessoria de Imprensa",
"Automação",
"Automotivo",
"Bancário / Financeiro",
"Bebidas",
"Bens de Capital",
"Bens de Consumo (Outros)",
"Borracha",
"Café",
"Calçados",
"Comércio Atacadista",
"Comércio Varejista",
"Comunicação",
"Concessionárias / Auto Peças",
"Construção Civil",
"Consultoria Geral",
"Contabilidade/ Auditoria",
"Corretagem (Imóveis)",
"Corretagem (Seguros)",
"Corretagem de Títulos e Valores Imobiliários",
"Cosméticos",
"Diversão/ Entretenimento",
"Educação/ Idiomas",
"Eletrônica/ Eletroeletrônica/ Eletrodomésticos",
"Embalagens",
"Energia/ Eletricidade",
"Engenharia",
"Equipamentos industriais",
"Equipamentos médicos / precisão",
"Estética/ Academias",
"Eventos",
"Farmacêutica/ Veterinária",
"Financeiras",
"Gráfica/ Editoras",
"Importação/ Exportação",
"Incorporadora",
"Indústrias",
"Informática",
"Internet/ Sites",
"Jornais",
"Jurídica",
"Logística / Armazéns",
"Madeiras",
"Materiais de Construção",
"Material de Escritório",
"Mecânica/ Manutenção",
"Metalúrgica / Siderúrgica",
"Mineração",
"Móveis e Artefatos de decoração",
"Órgãos públicos",
"Outros",
"Papel e Derivados",
"Petroquímico/ Petróleo",
"Plásticos",
"Prestadora de Serviços",
"Publicidade / Propaganda",
"Recursos Humanos",
"Relações Públicas",
"Representação Comercial",
"Restaurante/ Industrial/ Fast Food",
"Saúde",
"Segurança Patrimonial",
"Seguros/ Previdência Privada",
"Sindicatos / Associações / ONGs",
"Supermercado / Hipermercado",
"Telecomunicações",
"Telemarketing/ Call Center",
"Têxtil/ Couro",
"Transportes",
"Turismo/ Hotelaria",)


User = get_user_model()

DEFAULT_STATUS = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

# Produtos permitidos no perfil de acesso
DEFAULT_PRODUCT_NAME_GALCORR = (
    'Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional',
    'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)
DEFAULT_PRODUCT_NAME_PARTNER = (
    'Vida', 'Vida Global', 'Acidentes Pessoais', 'Garantia Tradicional',
    'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)
DEFAULT_PRODUCT_NAME_TOKIO = ('Vida', 'Vida Global', 'Acidentes Pessoais',)
DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS = ('Saúde',)
DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA = ('Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia',)

# Status x Perfil
DEFAULT_STATUS_PROFILE_TOKIO_SEE = (('Proposta Gerada', 1), ('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_TOKIO_EDIT = (('Proposta Gerada', 1), ('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_TOKIO_SET = (('Boleto Gerado', 2), ('Apólice Gerada', 3),)

DEFAULT_STATUS_PROFILE_PARTNER_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_PARTNER_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Lead de Benefícios Gerado', 2), ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_PARTNER_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6), ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_ADM_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_GER_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_EDIT = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2)
)

DEFAULT_STATUS_PROFILE_GALCORR_COM_SET = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),

    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),

    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2), ('Apólice Gerada', 3),
    ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_EDIT = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),

    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),

    ('Proposta Gerada', 1),
)

DEFAULT_STATUS_PROFILE_GALCORR_OPE_SET = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),

    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),

    ('Proposta Gerada', 1), ('Apólice Cancelada', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_SEE = (
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_EDIT = (
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECB_SET = (
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_EDIT = (
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_TECG_SET = (
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_SEE = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2),
    ('Solicitação de Cotação de Garantia', 3), ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2),
    ('Solicitação de Cotação de Benefícios', 3), ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
    ('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2),
    ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_EDIT = (
     ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),
)

DEFAULT_STATUS_PROFILE_GALCORR_FIN_SET = (
     ('Repasse Pago', 4),
)

# Produtos x Status Possíveis

DEFAULT_STATUS_PRODUCT_TOKIO = (('Proposta Gerada', 1), ('Proposta Cancelada', 2), ('Boleto Gerado', 2),
    ('Apólice Gerada', 3), ('Apólice Cancelada', 4), ('Repasse Pago', 4),)

DEFAULT_STATUS_PRODUCT_GARANTIA = (
    ('Lead de Garantia Gerado', 2), ('Lead de Garantia Cancelado', 2), ('Solicitação de Cotação de Garantia', 3),
    ('Cotação de Garantia Gerada', 4),
    ('Cotação de Garantia não Gerada - Faltam documentos', 4),
    ('Cotação de Garantia Negada', 5), ('Cotação de Garantia Aprovada', 6),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS = (
    ('Lead de Benefícios Gerado', 2), ('Lead de Benefícios Cancelado', 2), ('Solicitação de Cotação de Benefícios', 3),
    ('Cotação de Benefícios Gerada', 4),
    ('Cotação de Benefícios não Gerada - Faltam documentos', 4),
    ('Cotação de Benefícios Negada', 5), ('Cotação de Benefícios Aprovada', 6),
)

# Email x Status x Responsável x Produto

DEFAULT_STATUS_PRODUCT_TOKIO_EMAIL = (
    ('Proposta Gerada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Proposta Cancelada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Boleto Gerado', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Apólice Gerada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('lucia.moraes@galcorr.com.br', 'usr'),),),
    ('Apólice Cancelada', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('{Seguradora}', 'inc'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('lucia.moraes@galcorr.com.br', 'usr'),),),
    ('Repasse Pago', DEFAULT_PRODUCT_NAME_TOKIO,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',),),),)


DEFAULT_STATUS_PRODUCT_GARANTIA_EMAIL = (
    ('Lead de Garantia Gerado', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Lead de Garantia Cancelado', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Solicitação de Cotação de Garantia', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia Gerada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia não Gerada - Faltam documentos', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Garantia Negada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('rafael.nunes@comercialseguros.com.br', 'usr'), ('{Gerente}', 'own'),),),
    ('Cotação de Garantia Aprovada', DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('rafael.nunes@comercialseguros.com.br', 'usr'), ('{Gerente}', 'own'),),),
)

DEFAULT_STATUS_PRODUCT_BENEFICIOS_EMAIL = (
    ('Lead de Benefícios Gerado', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Lead de Benefícios Cancelado', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('{Gerente}', 'own'), ('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),),),
    ('Solicitação de Cotação de Benefícios', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'),),),
    ('Cotação de Benefícios Gerada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'),),),
    ('Cotação de Benefícios não Gerada - Faltam documentos', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('adriano.telles@galcorr.com.br', 'usr'), ('rafael.nunes@comercialseguros.com.br', 'usr'),),),
    ('Cotação de Benefícios Negada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('adriano.telles@galcorr.com.br', 'usr'), ('{Gerente}', 'own'),),),
    ('Cotação de Benefícios Aprovada', DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS,
     (('flavio.saraiva@galcorr.com.br', 'usr',), ('fabiano.costa@galcorr.com.br', 'usr',),
      ('adriano.telles@galcorr.com.br', 'usr'), ('{Gerente}', 'own'),),),
)

# Arquivos
DEFAULT_FILES = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Boleto de Apólice', 'Boleto de Endosso', 'Boleto de Apólice 2ª via', 'Boleto de Endosso 2ª via',
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_GALCORR = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_PARTNER = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Boleto de Apólice', 'Boleto de Endosso', 'Boleto de Apólice 2ª via', 'Boleto de Endosso 2ª via',
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_TOKIO = (
    'Proposta de Endosso', 'Proposta de Apólice', 'Endosso', 'Apólice',
    'Boleto de Apólice', 'Boleto de Endosso', 'Boleto de Apólice 2ª via', 'Boleto de Endosso 2ª via',
)

DEFAULT_FILES_GARANTIA = (
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_FILES_BENEFICIOS = (
    'Demonstrações financeiras de 2013 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2014 (assinadas e/ou auditadas)',
    'Demonstrações financeiras de 2015 (assinadas e/ou auditadas)',
    'Contrato/Estatuto Social e ata de eleição da última diretoria',
    'Fichas cadastrais preenchidas e assinadas',
    'Apresentação Institucional',
)

DEFAULT_INSURANCE = (('Tokio', '123456', 'r.cabral.n@gmail.com',), ('GalCorr', '000000', 'r.cabral.n@gmail.com',),)

DEFAULT_BRANCH = (
    'Vida', 'Acidentes Pessoais',
    'Garantia Tradicional', 'Garantia Judicial', 'Fiança Locatícia', 'Saúde',)

DEFAULT_PROFILE = (
    'Perfil Vida', 'Perfil Vida Global', 'Perfil Acidentes Pessoais', 'Perfil Garantia Tradicional',
    'Perfil Garantia Judicial', 'Perfil Fiança Locatícia', 'Perfil Saúde',)

# Produtos para serem incluídos
DEFAULT_PRODUCT = (
    ('Vida', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida',
        DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Vida', DEFAULT_STATUS_PRODUCT_TOKIO, 10, 10 , 10, 0, FULL_DECLARATION_VIDA, DECLARATION_VIDA,
        'Em caso de morte acidental, as coberturas básicas e IEA serão somadas', ('Boleto',), RULES_VIDA, RULEJS_VIDA, ),
    ('Vida Global', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Vida',
         DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Vida Global', DEFAULT_STATUS_PRODUCT_TOKIO, 10, 10 , 10, 0, FULL_DECLARATION_VIDA_GLOGAL, DECLARATION_VIDA_GLOGAL,
        'Em caso de morte acidental, as coberturas básicas e IEA serão somadas', ('Boleto',), RULES_VIDA_GLOBAL, RULEJS_VIDA_GLOBAL, ),
    ('Acidentes Pessoais', 'Introdução', 'Descrição', ' Declaração', 'J', 'Tokio', 'Acidentes Pessoais',
        DEFAULT_FILES_TOKIO,
        'Proposta Gerada', 'Perfil Acidentes Pessoais', DEFAULT_STATUS_PRODUCT_TOKIO, 10, 10, 10, 0, FULL_DECLARATION_AP, DECLARATION_AP, '', ('Boleto',), RULES_AP, RULEJS_AP, ),
    ('Garantia Tradicional', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Tradicional',
        DEFAULT_FILES_GARANTIA,
        'Lead de Garantia Gerado', 'Perfil Garantia Tradicional', DEFAULT_STATUS_PRODUCT_GARANTIA, 10, 10, 10, 1, '', '', '', ('Boleto',), '', '', ),
    ('Garantia Judicial', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Garantia Judicial',
         DEFAULT_FILES_GARANTIA,
        'Lead de Garantia Gerado', 'Perfil Garantia Judicial', DEFAULT_STATUS_PRODUCT_GARANTIA, 10, 10, 10, 1, '', '', '', ('Boleto',), '',  '', ),
    ('Fiança Locatícia', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Fiança Locatícia',
     DEFAULT_FILES_GARANTIA,
    'Lead de Garantia Gerado', 'Perfil Fiança Locatícia', DEFAULT_STATUS_PRODUCT_GARANTIA, 10, 10, 10, 1, '', '', '', ('Boleto',),  '',  '', ),
    ('Saúde', 'Introdução', 'Descrição', ' Declaração', 'F', 'GalCorr', 'Saúde',
     DEFAULT_FILES_BENEFICIOS,
    'Lead de Benefícios Gerado', 'Perfil Saúde', DEFAULT_STATUS_PRODUCT_BENEFICIOS, 10, 10, 10, 1, '', '', '', ('Boleto',),  '',  '', ),
    )

DEFAULT_PROFILE_NAME = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio',
)

PROFILE_NAME_PARTNER_ADM = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
)

PROFILE_NAME_PARTNER_DIR = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_PARTNER_SUP = (
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_PARTNER_GER = (
    'Perfil Parceiro Gerente',
)

PROFILE_NAME_TOKIO = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
)


PROFILE_NAME_GALCORR_ADM = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio',
)

PROFILE_NAME_GALCORR_GER = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio',
)

PROFILE_NAME_GALCORR_COM = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio',
)

PROFILE_NAME_GALCORR_OPE = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
)

PROFILE_NAME_GALCORR_TECB = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
)

PROFILE_NAME_GALCORR_TECG = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Garantia',
)

PROFILE_NAME_GALCORR_FIN = (
    'Perfil Parceiro Diretor',
    'Perfil Parceiro Supervisor',
    'Perfil Parceiro Gerente',
    'Perfil Parceiro Administrador',
    'Perfil GalCorr Administrador',
    'Perfil GalCorr Gerencial',
    'Perfil GalCorr Comercial',
    'Perfil GalCorr Operacional',
    'Perfil GalCorr Técnico Benefícios',
    'Perfil GalCorr Técnico Garantia',
    'Perfil GalCorr Financeiro',
    'Perfil Tokio',
)

DEFAULT_METHOD_PAYMENT = (
    ('Boleto', 'Após o envio da proposta, a seguradora irá gerar e enviar o boleto para pagamento',),)

DEFAULT_PROFILE_PERMISSION = (
    ('Perfil Parceiro Diretor', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_DIR,),
    ('Perfil Parceiro Supervisor', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_SUP,),
    ('Perfil Parceiro Gerente', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_GER,),
    ('Perfil Parceiro Administrador', 1, 1, 1, 1, (1, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_PARTNER, DEFAULT_STATUS_PROFILE_PARTNER_SEE, DEFAULT_STATUS_PROFILE_PARTNER_EDIT,
     DEFAULT_STATUS_PROFILE_PARTNER_SET, DEFAULT_FILES_PARTNER, DEFAULT_FILES_PARTNER, PROFILE_NAME_PARTNER_ADM,),
    ('Perfil GalCorr Administrador', 1, 1, 1, 1, (1, 1, 1, 1), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_ADM_SEE, DEFAULT_STATUS_PROFILE_GALCORR_ADM_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_ADM_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_ADM,),
    ('Perfil GalCorr Gerencial', 0, 0, 1, 0, (0, 0, 0, 0), 0, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_GER_SEE, DEFAULT_STATUS_PROFILE_GALCORR_GER_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_GER_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_GER,),
    ('Perfil GalCorr Comercial', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_COM_SEE, DEFAULT_STATUS_PROFILE_GALCORR_COM_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_COM_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_COM,),
    ('Perfil GalCorr Operacional', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_OPE_SEE, DEFAULT_STATUS_PROFILE_GALCORR_OPE_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_OPE_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_OPE,),
    ('Perfil GalCorr Técnico Benefícios', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR_BENEFICIOS, DEFAULT_STATUS_PROFILE_GALCORR_TECB_SEE,
     DEFAULT_STATUS_PROFILE_GALCORR_TECB_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_TECB_SET, DEFAULT_FILES_BENEFICIOS, DEFAULT_FILES_BENEFICIOS,
     PROFILE_NAME_GALCORR_TECB,),
    ('Perfil GalCorr Técnico Garantia', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR_GARANTIA, DEFAULT_STATUS_PROFILE_GALCORR_TECG_SEE,
     DEFAULT_STATUS_PROFILE_GALCORR_TECG_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_TECG_SET, DEFAULT_FILES_GARANTIA, DEFAULT_FILES_GARANTIA,
     PROFILE_NAME_GALCORR_TECG,),
    ('Perfil GalCorr Financeiro', 1, 0, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_GALCORR, DEFAULT_STATUS_PROFILE_GALCORR_FIN_SEE, DEFAULT_STATUS_PROFILE_GALCORR_FIN_EDIT,
     DEFAULT_STATUS_PROFILE_GALCORR_FIN_SET, DEFAULT_FILES_GALCORR, DEFAULT_FILES_GALCORR, PROFILE_NAME_GALCORR_FIN,),
    ('Perfil Tokio', 1, 1, 1, 0, (0, 0, 0, 0), 1, 1,
     DEFAULT_PRODUCT_NAME_TOKIO, DEFAULT_STATUS_PROFILE_TOKIO_SEE, DEFAULT_STATUS_PROFILE_TOKIO_EDIT,
     DEFAULT_STATUS_PROFILE_TOKIO_SET, DEFAULT_FILES_TOKIO, DEFAULT_FILES_TOKIO, PROFILE_NAME_TOKIO,),)


USERS = (
    ('Perfil Parceiro Diretor', '123', 'Sofisa', 'DiretorSofisa@mail.com', 'DiretorSofisa',),
    ('Perfil Parceiro Supervisor', '123', 'Sofisa', 'SupervisorSofisa@mail.com', 'SupervisorSofisa',),
    ('Perfil Parceiro Gerente', '123', 'Sofisa', 'GerenteSofisa@mail.com', 'GerenteSofisa',),
    ('Perfil Parceiro Administrador', '123', 'Sofisa', 'AdministradorSofisa@mail.com', 'AdministradorSofisa',),
    ('Perfil GalCorr Administrador', '123', 'GalCorr', 'fabiano.costa@galcorr.com.br', 'AdministradorGalCorr',),
    ('Perfil GalCorr Gerencial', '123', 'GalCorr', 'GerenteGalCorr@mail.com', 'GerenteGalCorr',),
    ('Perfil GalCorr Comercial', '123', 'GalCorr', 'flavio.saraiva@galcorr.com.br', 'ComercialGalCorr',),
    ('Perfil GalCorr Operacional', '123', 'GalCorr', 'lucia.moraes@galcorr.com.br', 'OperacionalGalCorr',),
    ('Perfil GalCorr Técnico Benefícios', '123', 'GalCorr', 'adriano.telles@galcorr.com.br', 'TecnicoBeneficiosGalCorr',),
    ('Perfil GalCorr Técnico Garantia', '123', 'GalCorr', 'rafael.nunes@comercialseguros.com.br', 'TecnicoGarantiaGalCorr',),
    ('Perfil GalCorr Financeiro', '123', 'GalCorr', 'FinanceiroGalCorr@mail.com', 'FinanceiroGalCorr',),
    ('Perfil Tokio', '123', 'GalCorr', 'r.cabral.n@gmail.com', 'TokioMarine',),
)


class Command(BaseCommand):
    help = 'Cria dados padrões para o início da aplicação'

    def handle(self, *args, **options):

        if Partner.objects.filter(id=1).exists():
            p = Partner.objects.get(id=1)
        else:
            s = Site(domain='sofisa', name='Sofisa')
            s.save()
            p = Partner(
                name='Sofisa',
                email='sofisa@mail.com',
                cnpj='60.889.128.0001-80',
                site=s,
                internal_code='00000',
                operational_code='00000',
            )
            p.save()

        if Partner.objects.filter(id=2).exists():
            p = Partner.objects.get(id=2)
        else:
            s = Site(domain='galcorr', name='GalCorr')
            s.save()
            p = Partner(
                name='GalCorr',
                email='GalCorr@mail.com',
                cnpj='00.000.000.0000-00',
                site=s,
                internal_code='00000',
                operational_code='00000',
            )
            p.save()

        if Partner.objects.filter(id=3).exists():
            p = Partner.objects.get(id=3)
        else:
            s = Site(domain='tokio', name='Tokio')
            s.save()
            p = Partner(
                name='Tokio',
                email='Tokio@mail.com',
                cnpj='00.000.000.0000-00',
                site=s,
                internal_code='00000',
                operational_code='00000',
            )
            p.save()

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin", partner=p)

        if not User.objects.filter(username="demo").exists():
            u = User(username="demo", email="demo@demo.com", password="massificadodemo", partner=p)
            u.save()

        for user_profile, user_password, user_partner, user_email, user_name in USERS:
            if not MassificadoUser.objects.filter(email=user_email).exists():
                user = MassificadoUser(username=user_name,
                                       email=user_email,
                                       password=user_password,
                                       partner=Partner.objects.get(name=user_partner))
                user.save()

        for area_name in AREA:
            if not ActivityArea.objects.filter(name=area_name).exists():
                ar = ActivityArea(name=area_name)
                ar.save()

        for method, disclaimer in DEFAULT_METHOD_PAYMENT:
            if not MethodPayment.objects.filter(name=method).exists():
                mt = MethodPayment(name=method, disclaimer=disclaimer)
                mt.save()

        for status_name, level in DEFAULT_STATUS:
            if not Status.objects.filter(name=status_name).exists():
                st = Status(name=status_name, level=level)
                st.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for file_name in DEFAULT_FILES:
            if not FileType.objects.filter(name=file_name).exists():
                fl = FileType(name=file_name)
                fl.save()

        for cia, susep, email in DEFAULT_INSURANCE:
            if not InsuranceCompany.objects.filter(name=cia).exists():
                insurance_company = InsuranceCompany(name=cia, susep=susep, email=email)
                insurance_company.save()

        for branch_name in DEFAULT_BRANCH:
            if not Branch.objects.filter(name=branch_name).exists():
                branch = Branch(name=branch_name)
                branch.save()

        for profile_name in DEFAULT_PROFILE:
            if not Profile.objects.filter(name=profile_name).exists():
                pe = Profile(name=profile_name)
                pe.save()

        for rule_name, rule_percent, rule_rate, rule_fixing_text, rule_type, rule_value, rule_rule in RULES_DEFAULT:
            if not RuleProduct.objects.filter(name=rule_name).exists():
                r = RuleProduct(name=rule_name,
                                percent=rule_percent,
                                rate=rule_rate,
                                fixing_text=rule_fixing_text,
                                type=rule_type,
                                value=rule_value,
                                rule=rule_rule,
                                )
                r.save()

        for p_number in range(501):
            if not NumberLives.objects.filter(number=p_number).exists():
                if p_number > 0:
                    p = NumberLives(number=p_number)
                    p.save()

        # for profile in DEFAULT_PROFILE_NAME:
        #     if not MassificadoGroups.objects.filter(name=profile).exists():
        #         per = MassificadoGroups(name=profile)
        #         per.save()

        for product_name, introduction, description, declaration, kind, insurance, branch, files,\
        begin, profile, status_permitted, partner_percentage, owner_percentage, master_percentage, is_lead,\
        p_declaration_full,  p_declaration, p_rules_declaration, p_methods, p_rules, p_rules_js in DEFAULT_PRODUCT:
            if not Product.objects.filter(name=product_name).exists():
                product = Product(
                    name=product_name,
                    introduction=introduction,
                    description=description,
                    declaration=declaration,
                    kind_person=kind,
                    insurance_company=InsuranceCompany.objects.get(name=insurance),
                    branch=Branch.objects.get(name=branch),
                    begin_status=Status.objects.get(name=begin),
                    profile=Profile.objects.get(name=profile),
                    partner_percentage=partner_percentage,
                    owner_percentage=owner_percentage,
                    master_percentage=master_percentage,
                    is_lead=is_lead,
                    rules_declaration=p_rules_declaration,
                    rules_js=p_rules_js,
                )
                product.full_declaration = p_declaration_full
                product.declaration = p_declaration
                product.other_documents_declaration ='Outros documentos poderão ser solicitados durante o processo'
                product.disclaimer = 'Após o envio da proposta, a seguradora irá gerar e enviar o boleto para pagamento'
                product.save()

                for rule in p_rules:
                    product.rules.add(RuleProduct.objects.get(name=rule))

                for method in p_methods:
                    product.method_payment.add(MethodPayment.objects.get(name=method))

                for file in files:
                    product.file_type.add(FileType.objects.get(name=file))

                for status_p, level in status_permitted:
                    product.status_permission.add(Status.objects.get(name=status_p))

                for status_p, lever in status_permitted:
                    action_st = ActionStatus(
                             product=product,
                             status=Status.objects.get(name=status_p))
                    action_st.save()
                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_TOKIO_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_BENEFICIOS_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

                    for st, products_emails, emails in DEFAULT_STATUS_PRODUCT_GARANTIA_EMAIL:
                        if st == status_p:
                            for product_emails in products_emails:
                                if product_emails == product_name:
                                    for email, type in emails:
                                        action_st_email = ActionStatusEmails(action_status=action_st, action_email=type)
                                        action_st_email.save()
                                        if type == 'usr':
                                            if User.objects.filter(email=email).exists():
                                                action_st_email_user = ActionStatusEmailsUsers(
                                                    action_status_email=action_st_email,
                                                    user=User.objects.get(email=email))
                                                action_st_email_user.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries,\
            menu_active_entries_detail, menu_active_notification, menu_active_profile, products_permission,\
            status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission,\
            filetype_download_permission, profile_names_permission in DEFAULT_PROFILE_PERMISSION:

            if not MassificadoGroups.objects.filter(name=permission_name).exists():
                group = MassificadoGroups(
                    name=permission_name,
                    menu_products=menu_active_product,
                    menu_dashboard=menu_active_dashboard,
                    menu_production=menu_active_production,
                    menu_entries=menu_active_entries,
                    menu_notification=menu_active_notification,
                    menu_profile=menu_active_profile

                )
                group.menu_entries_users = menu_active_entries_detail[0]
                group.menu_entries_profiles = menu_active_entries_detail[1]
                group.menu_entries_partners = menu_active_entries_detail[2]
                group.menu_entries_products = menu_active_entries_detail[3]

                group.save()

        for permission_name, menu_active_product, menu_active_dashboard, menu_active_production, menu_active_entries,\
            menu_active_entries_detail, menu_active_notification, menu_active_profile, products_permission,\
            status_see_permission, status_edit_permission, status_set_permission, filetype_see_permission,\
            filetype_download_permission, profile_names_permission in DEFAULT_PROFILE_PERMISSION:

                 if MassificadoGroups.objects.filter(name=permission_name).exists():
                    group = MassificadoGroups.objects.get(name=permission_name)

                    for products_p in products_permission:
                        group.product.add(Product.objects.get(name=products_p))

                    for status_see_p_name, level in status_see_permission:
                         group.status_see.add(Status.objects.get(name=status_see_p_name))

                    for status_edit_p_name, level in status_edit_permission:
                        group.status_edit.add(Status.objects.get(name=status_edit_p_name))

                    for status_set_p_name, level in status_set_permission:
                        group.status_set.add(Status.objects.get(name=status_set_p_name))

                    for filetype_see_p in filetype_see_permission:
                        group.filetype_see.add(FileType.objects.get(name=filetype_see_p))

                    for filetype_download_p in filetype_download_permission:
                        group.filetype_download.add(FileType.objects.get(name=filetype_download_p))

                    group.profiles.clear()
                    for profile_names_p in profile_names_permission:
                        group.profiles.add(MassificadoGroups.objects.get(name=profile_names_p))

                    group.save()

        for user_profile, user_password, user_partner, user_email, user_name in USERS:
                user = MassificadoUser.objects.get(email=user_email)
                user.set_password('galcorr')
                user.group_permissions = MassificadoGroups.objects.get(name=user_profile)
                if "Parceiro" in user_profile:
                    user.master = MassificadoUser.objects.get(username='SupervisorSofisa')
                user.save()


