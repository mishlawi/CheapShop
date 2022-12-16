import java.util.ArrayList;
import java.util.List;

public class Produto {
    private String strToda;
    private String nome;
    private String marca;
    private String quantidade;
    private String preco;
    private String ppu;
    private String promo;
    private String EANOriginal;
    private List<String> EANCopiados;

//Nome,Marca,Quantidade,Preço Primário,Preço Por Unidade,Promo,EAN
//ESPONJA JEAN LOUIS DAVID URBAN BEAUTY 4UN,JEAN LOUIS DAVID,4UN,3.29€,0.82 €/un,None,3666085112518


    public boolean temEstaMarca(String a){ //devolve true se for a mesma marca e diferente de NONE
        if (this.getMarca().equals("NONE") || this.getMarca().equals("z") || a.equals("NONE")  || a.equals("") || a.isEmpty() )
                return false;

        else{
            return this.getMarca().equals(a);
        }

    }


    public Produto() {
        this.strToda="z";
        this.nome="z";
        this.marca="z";
        this.quantidade="z";
        this.preco="z";
        this.ppu="z";
        this.promo="z";
        this.EANOriginal="z";
        this.EANCopiados=new ArrayList<>(3);


    }

    public Produto(String strToda, String nome, String marca, String quantidade, String preco, String ppu, String promo) {
        this.strToda = strToda;
        this.nome = nome;
        this.marca = marca;
        this.quantidade = quantidade;
        this.preco = preco;
        this.ppu = ppu;
        this.promo = promo;
        this.EANOriginal="z";
        this.EANCopiados=new ArrayList<>(3);
    }

    public Produto(String strToda, String nome, String marca, String quantidade, String preco, String ppu) {
        this.strToda = strToda;
        this.nome = nome;
        this.marca = marca;
        this.quantidade = quantidade;
        this.preco = preco;
        this.ppu = ppu;
        this.promo = "z";
        this.EANOriginal="z";
        this.EANCopiados=new ArrayList<>(3);
    }


    @Override
    public String toString() {
        return "Produto{  " +
                 strToda + '\'' +
                "  }";
    }

    public String getEANOriginal() {
        return EANOriginal;
    }

    public List<String> getEANCopiados() {
        return this.EANCopiados;
    }

    public void setEANOriginal(String EANOriginal) {
        this.EANOriginal = EANOriginal;
    }

    public void addEANCopiado(String EAN) {
        this.EANCopiados.add(EAN);
    }

    public String getStrToda() {
        return strToda;
    }

    public void setStrToda(String strToda) {
        this.strToda = strToda;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getMarca() {
        return marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    public String getQuantidade() {
        return quantidade;
    }

    public void setQuantidade(String quantidade) {
        this.quantidade = quantidade;
    }

    public String getPreco() {
        return preco;
    }

    public void setPreco(String preco) {
        this.preco = preco;
    }

    public String getPpu() {
        return ppu;
    }

    public void setPpu(String ppu) {
        this.ppu = ppu;
    }

    public String getPromo() {
        return promo;
    }

    public void setPromo(String promo) {
        this.promo = promo;
    }
}
