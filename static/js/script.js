const btnUp = {
    el: document.querySelector('.up'),
    show() {
      this.el.classList.remove('up__hide');
    },
    hide() {
      this.el.classList.add('up__hide');
    },
    addEventListener() {
      window.addEventListener('scroll', () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop;
        scrollY > 200 ? this.show() : this.hide();
      });
      document.querySelector('.up').onclick = () => {
        window.scrollTo({
          top: 0,
          left: 0,
          behavior: 'smooth'
        });
      }
    }
  }

  btnUp.addEventListener();

  const btnUpp = {
    el: document.querySelector('.up__top'),
    show() {
      this.el.classList.remove('up__hide');
    },
    hide() {
      this.el.classList.add('up__hide');
    },
    addEventListener() {
      window.addEventListener('scroll', () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop;
        scrollY > 200 ? this.show() : this.hide();
      });
      document.querySelector('.up__top').onclick = () => {
        window.scrollTo({
          top: 0,
          left: 0,
          behavior: 'smooth'
        });
      }
    }
  }

  btnUpp.addEventListener();