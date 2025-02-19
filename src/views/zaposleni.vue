<script>
import axios from 'axios';

export default {
    data() {
        return {
            zaposleni: [],
            noviZaposleni: {
                imeiprezime: '',
                pozicija: '',
                datumzaposlenja: '',
                email: '',
                kontakt: ''
            }
        };
    },
    methods: {
        async fetchZaposleni() {
            try {
                const token = localStorage.getItem("token"); // Dohvati token ako postoji
                const response = await axios.get('http://localhost:5000/api/zaposleni', {
                    headers: token ? { Authorization: `Bearer ${token}` } : {},
                    withCredentials: true
                });
                this.zaposleni = response.data;
            } catch (error) {
                console.error("❌ Greška pri dobavljanju zaposlenih:", error.response ? error.response.data : error.message);
            }
        },
        async dodajZaposlenog() {
            try {
                const token = localStorage.getItem("token");
                await axios.post('http://localhost:5000/api/dodaj_zaposlenog', this.noviZaposleni, {
                    headers: token ? { Authorization: `Bearer ${token}` } : {},
                    withCredentials: true
                });
                this.fetchZaposleni(); // Osvježavanje liste nakon dodavanja
                alert("✅ Zaposleni uspešno dodat!");
                this.noviZaposleni = { imeiprezime: '', pozicija: '', datumzaposlenja: '', email: '', kontakt: '' };
            } catch (error) {
                console.error("❌ Greška pri dodavanju zaposlenog:", error.response ? error.response.data : error.message);
            }
        }
    },
    mounted() {
        this.fetchZaposleni();
    }
};
</script>

<template>
    <div class="container">
        <h1>Zaposleni</h1>
        <table class="table">
            <thead>
                <tr>
                    <th>Ime i prezime</th>
                    <th>Pozicija</th>
                    <th>Datum zaposlenja</th>
                    <th>Email</th>
                    <th>Kontakt</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="z in zaposleni" :key="z.id">
                    <td>{{ z.ime }} {{ z.prezime }}</td>
                    <td>{{ z.pozicija }}</td>
                    <td>{{ z.datum_zaposlenja }}</td>
                    <td>{{ z.mejl }}</td>
                    <td>{{ z.kontakt }}</td>
                </tr>
            </tbody>
        </table>

        <h2>Dodaj zaposlenog</h2>
        <form @submit.prevent="dodajZaposlenog">
            <input v-model="noviZaposleni.imeiprezime" placeholder="Ime i prezime" required />
            <input v-model="noviZaposleni.pozicija" placeholder="Pozicija" required />
            <input type="date" v-model="noviZaposleni.datumzaposlenja" required />
            <input v-model="noviZaposleni.email" placeholder="Email" required />
            <input v-model="noviZaposleni.kontakt" placeholder="Kontakt" required />
            <button type="submit">Dodaj</button>
        </form>
    </div>
</template>
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
