<template>
  <div class="container">
    <h2>RASPORED RADNIKA</h2>
    <!-- Padajuća lista za menadžera -->
    <div v-if="isMenadzer" class="select-container">
      <p v-if="!odabraniZaposleniId" class="text-muted">
        Izaberite zaposlenog da biste videli njegov raspored.
      </p>
      <select
        v-model="odabraniZaposleniId"
        class="custom-select"
        @change="fetchRaspored"
      >
        <option value="">Izaberite zaposlenog</option>
        <option
          v-for="zaposleni in zaposleniLista"
          :key="zaposleni.id"
          :value="zaposleni.id"
        >
          {{ zaposleni.ime }} {{ zaposleni.prezime }}
        </option>
      </select>
    </div>
    <!-- Tabela rasporeda se prikazuje kada postoji odabran ID zaposlenog -->
    <div v-if="odabraniZaposleniId">
      <table class="table table-bordered mt-4">
        <thead>
          <tr>
            <th>Dan</th>
            <th v-for="(termin, index) in termini" :key="index">
              <!-- Ako je index 3, to je pauza -->
              {{ index === 3 ? "12:30 - 13:00" : termin }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dan in dani" :key="dan">
            <td>{{ dan }}</td>
            <td v-for="(termin, index) in termini" :key="index">
              <!-- Ako je kolona pauza -->
              <span v-if="index === 3">Pauza</span>
              <span v-else-if="raspored[dan] && raspored[dan][termin]">
                {{ raspored[dan][termin] }}
              </span>
              <span v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="text-muted">Nema podataka za odabranog radnika.</p>
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
        "12:30 - 13:00", // Pauza
        "13:00 - 14:30",
        "14:30 - 16:00",
      ],
      zaposleniLista: [],
      raspored: {},
      odabraniZaposleniId: "",
      // Postavi na true ako testiraš kao menadžer, a false za radnika
      isMenadzer: false,
    };
  },
  methods: {
    async fetchZaposleni() {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/radnik_raspored",
          { withCredentials: true }
        );
        this.zaposleniLista = response.data.zaposleni_lista;
        console.log(response.data);
      } catch (error) {
        console.error("Greška pri učitavanju zaposlenih:", error);
      }
    },
    async fetchRaspored() {
      if (!this.odabraniZaposleniId) {
        console.warn("Nema odabranog zaposlenog ID!");
        return;
      }
      try {
        const response = await axios.get(
          `http://localhost:5000/api/radnik_raspored/${this.odabraniZaposleniId}`,
          { withCredentials: true }
        );
        // Proširena mapa koja pokriva oba formata vremena: "08:00:00" i "8:00"
        const mapiranoVreme = {
          "08:00:00": "08:00 - 09:30",
          "8:00": "08:00 - 09:30",
          "09:30:00": "09:30 - 11:00",
          "9:30": "09:30 - 11:00",
          "11:00:00": "11:00 - 12:30",
          "11:00": "11:00 - 12:30",
          "13:00:00": "13:00 - 14:30",
          "13:00": "13:00 - 14:30",
          "14:30:00": "14:30 - 16:00",
          "14:30": "14:30 - 16:00",
        };
        let noviRaspored = {};
        // Iteriramo kroz raspored dobijen iz backend-a
        for (let dan in response.data.raspored) {
          noviRaspored[dan] = {};
          for (let termin in response.data.raspored[dan]) {
            // Mapiramo originalni termin na slot – podržavamo oba formata
            let noviTermin = mapiranoVreme[termin] || termin;
            noviRaspored[dan][noviTermin] = response.data.raspored[dan][termin];
          }
        }
        this.raspored = noviRaspored;
      } catch (error) {
        console.error("Greška pri učitavanju rasporeda:", error);
      }
    },
  },
  mounted() {
    if (this.isMenadzer) {
      // Ako je menadžer, učitaj listu zaposlenih; raspored se učitava pri odabiru zaposlenog.
      this.fetchZaposleni();
    } else {
      const storedId = localStorage.getItem("ulogovan_id");
      this.odabraniZaposleniId = Number(storedId);
      this.fetchRaspored();
    }
  },
};
</script>

<style scoped>
.container {
    padding: 20px;
    text-align: center;
}
.title {
    color: #D4AF37;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 15px;
}
.subtitle {
    color: #B8860B;
    font-size: 22px;
    margin-top: 20px;
}
.table {
    width: 100%;
    border-collapse: collapse;
    background-color: #fff;
    margin-top: 20px;
}
.table th, .table td {
    border: 1px solid #ccc;
    padding: 12px;
    text-align: left;
}
.table th {
    background-color: #D4AF37;
    color: white;
}
tr:nth-child(even) {
    background-color: #f9f9f9;
}
tr:hover {
    background-color: #f1f1f1;
}
.form-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 400px;
    margin: auto;
}
.input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
.button {
    padding: 10px;
    background-color: #D4AF37;
    border: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px;
}
.button:hover {
    background-color: #B8860B;
}
</style>
