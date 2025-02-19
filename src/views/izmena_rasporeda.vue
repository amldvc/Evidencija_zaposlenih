<template>
  <div class="container">
    <h2>IZMENA RASPOREDA</h2>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Dan</th>
          <th>08:00 - 09:30</th>
          <th>09:30 - 11:00</th>
          <th>11:00 - 12:30</th>
          <th>PAUZA</th>
          <th>13:00 - 14:30</th>
          <th>14:30 - 16:00</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dan in dani" :key="dan">
          <td>{{ dan }}</td>
          <td v-for="termin in termini" :key="termin">
            <strong v-if="termin === 'PAUZA'">PAUZA</strong>
            <div v-else>
              <div
                v-if="raspored[dan] && raspored[dan][termin]"
                class="d-flex align-items-center"
              >
                <span class="me-2"
                  ><strong>{{ raspored[dan][termin].zaposleni }}</strong></span
                >
                <button
                  @click="obrisiTermin(raspored[dan][termin].id)"
                  class="btn btn-danger btn-sm"
                >
                  X
                </button>
              </div>
              <form v-else @submit.prevent="dodajTermin(dan, termin)">
                <select
                  v-model="novaRezervacija.zaposleni_id"
                  class="form-select form-select-sm"
                  required
                >
                  <option value="" disabled selected>
                    Izaberite zaposlenog
                  </option>
                  <option
                    v-for="zaposleni in zaposleni_lista"
                    :key="zaposleni.id"
                    :value="zaposleni.id"
                  >
                    {{ zaposleni.ime }} {{ zaposleni.prezime }}
                  </option>
                </select>
                <input
                  v-model="novaRezervacija.klijent"
                  type="text"
                  placeholder="Klijent"
                  class="form-control form-control-sm mt-1"
                  required
                />
                <button type="submit" class="btn btn-sm btn-warning mt-1">
                  Dodaj
                </button>
              </form>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="flashMessages.length">
      <div
        v-for="(message, index) in flashMessages"
        :key="index"
        class="alert alert-success alert-dismissible fade show flash-message"
      >
        <span class="bubble">{{ message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      dani: ["Ponedeljak", "Utorak", "Sreda", "Četvrtak", "Petak"],
      termini: [
        "08:00 - 09:30",
        "09:30 - 11:00",
        "11:00 - 12:30",
        "PAUZA",
        "13:00 - 14:30",
        "14:30 - 16:00",
      ],
      raspored: {},
      zaposleni_lista: [],
      novaRezervacija: {
        zaposleni_id: "",
        klijent: "",
      },
      flashMessages: [],
    };
  },
  methods: {
    async fetchPodaci() {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/izmena_rasporeda"
        );
        this.raspored = response.data.raspored;
        this.zaposleni_lista = response.data.zaposleni_lista;
        console.log(response.data);
      } catch (error) {
        console.error("Greška pri učitavanju podataka:", error);
      }
    },
    async dodajTermin(dan, termin) {
      // Pretpostavljamo da je termin oblika "08:00 - 09:30"
      const skraceniTermin = termin.split(" - ")[0]; // dobija "08:00"

      try {
        const response = await axios.post(
          "http://localhost:5000/api/izmena_rasporeda",
          {
            dan,
            termin: skraceniTermin,
            zaposleni_id: this.novaRezervacija.zaposleni_id,
            klijent: this.novaRezervacija.klijent,
          }
        );
        this.flashMessages.push(response.data.message);
        this.novaRezervacija.zaposleni_id = "";
        this.novaRezervacija.klijent = "";
        this.fetchPodaci();
      } catch (error) {
        console.error("Greška pri dodavanju termina:", error);
      }
    },
    async obrisiTermin(dan, termin) {
      try {
        const termin_id = this.raspored[dan][termin].id; // Dohvati termin_id

        await axios.delete("http://localhost:5000/api/obrisi_termin", {
          data: { termin_id }, // Axios DELETE mora imati `data`
        });

        this.flashMessages.push("Termin uspešno obrisan!");
        this.fetchPodaci();
      } catch (error) {
        console.error("Greška pri brisanju termina:", error);
      }
    },
  },
  mounted() {
    this.fetchPodaci();
  },
};
</script>
