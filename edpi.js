// EDPI calculator (EDPI page). The formulas follow the ElevateX Drive Performance Index framework.
// The page shows the worked example's numbers without JavaScript; this keeps them live as values change.
const EDPI_SETTINGS = {
  normalCost: 53.42,
  overspendStart: 1.0,
  overspendZero: 1.5,
  turnoutMax: 150,
  wMoney: 0.25,
  wVolunteer: 0.25,
  wImpact: 0.5,
  partnerBonusMax: 10,
};

function edpiScore(v, s = EDPI_SETTINGS) {
  const notes = [];
  // Step 1: basic figures
  const avgHours = v.volunteers > 0 ? v.totalHours / v.volunteers : 0;
  const budgetUsed = v.spent / v.budget;
  // Step 2: four scores
  let costScore;
  if (v.peopleHelped === 0) { costScore = 0; notes.push('No people helped, so the cost score is 0 and the drive would be flagged.'); }
  else if (v.spent === 0) costScore = 100;
  else {
    const costPerPerson = v.spent / v.peopleHelped;
    costScore = costPerPerson <= s.normalCost ? 100 : (100 * s.normalCost) / costPerPerson;
  }
  let budgetScore;
  if (budgetUsed <= s.overspendStart) budgetScore = 100;
  else if (budgetUsed >= s.overspendZero) { budgetScore = 0; notes.push('Spending was over 1.5 times the budget, so the drive would be flagged for review.'); }
  else budgetScore = 100 - (100 * (budgetUsed - s.overspendStart)) / (s.overspendZero - s.overspendStart);
  let turnoutScore = 0;
  let timeScore = 0;
  if (v.volunteers > 0) {
    turnoutScore = Math.min((100 * v.volunteers) / v.plannedVolunteers, s.turnoutMax);
    timeScore = avgHours <= v.plannedHours ? 100 : (100 * v.plannedHours) / avgHours;
    if (avgHours < 0.5 || avgHours > 24) notes.push('Average hours per volunteer are outside 0.5 to 24, so the hours would be flagged for review.');
  } else {
    notes.push('No volunteers, so the turnout, time and volunteer scores are 0.');
  }
  // Step 3: pillars and bonus
  const money = Math.sqrt(costScore * budgetScore);
  const volunteer = turnoutScore + timeScore > 0 ? (2 * turnoutScore * timeScore) / (turnoutScore + timeScore) : 0;
  const impact = v.impactDone >= v.impactTarget ? 100 : (100 * v.impactDone) / v.impactTarget;
  const bonus = v.hasPartner ? s.partnerBonusMax : 0;
  // Step 4: final index
  const total = s.wMoney * money + s.wVolunteer * volunteer + s.wImpact * impact + bonus;
  return { total, money, volunteer, impact, bonus, notes };
}

(function () {
  const form = document.getElementById('edpiCalc');
  if (!form) return;
  const out = document.getElementById('edpiScore');
  const parts = document.getElementById('edpiParts');
  const note = document.getElementById('edpiNote');
  const num = (name) => Number(form.elements[name].value);
  const fmt = (n) => (Math.round(n * 100) / 100).toFixed(2);
  const update = () => {
    const v = {
      plannedVolunteers: num('plannedVolunteers'), plannedHours: num('plannedHours'), budget: num('budget'),
      impactTarget: num('impactTarget'), hasPartner: form.elements.hasPartner.checked,
      spent: num('spent'), peopleHelped: num('peopleHelped'), volunteers: num('volunteers'),
      totalHours: num('totalHours'), impactDone: num('impactDone'),
    };
    const planning = ['plannedVolunteers', 'plannedHours', 'budget', 'impactTarget'];
    const results = ['spent', 'peopleHelped', 'volunteers', 'totalHours', 'impactDone'];
    if (planning.some((k) => !(v[k] > 0)) || results.some((k) => !(v[k] >= 0) || Number.isNaN(v[k]))) {
      out.textContent = '–';
      note.textContent = 'Planning values must be more than 0, and results 0 or more.';
      return;
    }
    const r = edpiScore(v);
    out.textContent = fmt(r.total);
    const dd = parts.querySelectorAll('dd');
    dd[0].textContent = fmt(r.money);
    dd[1].textContent = fmt(r.volunteer);
    dd[2].textContent = fmt(r.impact);
    dd[3].textContent = String(r.bonus);
    note.textContent = r.notes.join(' ');
  };
  form.addEventListener('input', update);
  form.addEventListener('submit', (e) => e.preventDefault());
  update();
})();

if (typeof module !== 'undefined') module.exports = { edpiScore, EDPI_SETTINGS };
