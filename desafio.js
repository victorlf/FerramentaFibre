"use strict";

// Modelo de informação
var facts = [
  ['gabriel', 'endereço', 'av rio branco, 109', true],
  ['joão', 'endereço', 'rua alice, 10', true],
  ['joão', 'endereço', 'rua bob, 88', true],
  ['joão', 'telefone', '234-5678', true],
  ['joão', 'telefone', '91234-5555', true],
  ['joão', 'telefone', '234-5678', false],
  ['gabriel', 'telefone', '98888-1111', true],
  ['gabriel', 'telefone', '98888-1111', false],
  ['gabriel', 'telefone', '98888-1111', true],
  ['gabriel', 'telefone', '56789-1010', true],
];

// Cadinalidade de cada tipo de informação
var schema = [
    ['endereço', 'cardinality', 'one'],
    ['telefone', 'cardinality', 'many']
];

// Retorna as informações vigentes
function fatosVigentes(facts, schema)
{

  // Retira do modelo todos que tiverem ação de remoção (false)
  remocao(facts);

  // Verifica a cardinalidade de cada tipo de informação e a aplica
  schema.forEach(function(cardinalidade){

    // Caso só possa ter uma informação com essa propriedade
    if (cardinalidade[2] === "one")
      // Retira as inserções mais antigas 
      one_to_one(cardinalidade[0], facts);  

  })

  // Retorna o modelo de informação final
  console.log(facts);
}

function remocao(facts)
{
  // Percorre facts
  for (var i = 0; i < facts.length; i++)
  {
    // Caso a informação tenha propriedade de remoção 
    if (facts[i][3] === false)
    {
      // Percorre as informações anteriores
      for (var j = 0; j < i; j++) 
      {
        // Quando encontrar a(s) inserção(s) dessa informação
        if (facts[j][0] === facts[i][0] && facts[j][2] === facts[i][2])
        {
          // Retira a ação de inserção (true)
          facts.splice(j, 1);

          // Retira a ação de remoção
          facts.splice(i - 1, 1);

          // Mantém a posição do loop
          if (i === 1)
            i = 0;
          else
            i = i - 2;
        }
      }
    }
  }
}

// Retira as informação mais antigas com a mesma propriedade para a mesma pessoa
function one_to_one(propriedade, facts)
{
  // Percorre facts
  for(var i = 0; i < facts.length; i++){
    // Caso a informação tenha essa propriedade
    if (facts[i][1] === propriedade)
    {
      // Percorre as informações posteriores
      for (var k = i + 1; k < facts.length; k++)
      {
        // Caso uma delas tenha propriedade similarar para mesma pessoa
        if (propriedade === facts[k][1] && facts[i][0] === facts[k][0])
        {
          // Retira a mais antiga
          facts.splice(i, 1);

          // Caso o primeiro elemento de facts precise ser retirado
          if (i != 0)
            i = i - 1;
        }
      }
    }
  }
}



fatosVigentes(facts, schema);
