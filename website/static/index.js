function deleteAktivitas(IdAktivitas) {
    fetch("/delete-aktivitas", {
      method: "POST",
      body: JSON.stringify({ IdAktivitas: IdAktivitas }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }