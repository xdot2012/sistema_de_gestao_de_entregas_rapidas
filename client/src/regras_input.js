const defaultTextRegex = (str) => /^[A-Za-zÀ-ÖØ-öø-ÿ ]+$/.test(str);
const phoneNumberRegex = (str) => /^[0-9()-- ]+$/.test(str);
const numbersRegex = (str) => /^[0-9]+$/.test(str);
const numbersHifexRegex = (str) => /^[0-9-]+$/.test(str);

export const regraTelefone = [
  (value) => !!value || 'Required.',
  (value) => (value && value.length >= 14) || 'Min 11 characters',
  (value) => phoneNumberRegex(value) || 'Caractere Inválido',
];

export const regraNomeCliente = [
  (value) => !!value || 'Required.',
  (value) => (value && value.length >= 3) || 'Min 3 characters',
  (value) => defaultTextRegex(value) || 'Caractere Inválido',
];

export const regraNumero = [
  (value) => !!value || 'Required.',
  (value) => numbersRegex(value) || 'Caractere Inválido',
];

export const regraCEP = [
  (value) => !!value || 'Required.',
  (value) => numbersHifexRegex(value) || 'Caractere Inválido',
];

export const regraTexto = [
  (value) => !!value || 'Required.',
  (value) => defaultTextRegex(value) || 'Caractere Inválido',
];
