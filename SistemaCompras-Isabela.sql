drop database sistema_compras;
create database sistema_compras;
use sistema_compras;

create table conta_cliente(
	id_cliente int not null auto_increment,
    CPF bigint(11) not null,
    nome varchar(100) not null,
    telefone bigint(11) not null,
    usuario_web enum('S', 'N') not null,
    primary key (id_cliente)
) auto_increment = 12345;
select * from conta_cliente;

create table usuarioWeb(
	nome_login varchar(20) not null,
	id_cliente int not null,
    status_conta enum('novo', 'ativo', 'bloqueado', 'banido', 'excluido') not null,
    email_cliente varchar(50) not null,
    senha varchar(30) not null,
    foreign key (id_cliente) references conta_cliente(id_cliente),
    primary key (nome_login)
);
select * from usuarioWeb;

create table enderecos(
	id_endereco int not null auto_increment,
	rua varchar(100) null,
    numero integer(5) null,
    bairro varchar(100) null,
    cidade varchar(100) null,
    estado varchar(2) null,
    cep integer(8) null,
    id_cliente int not null,
    foreign key (id_cliente) references conta_cliente(id_cliente),
    primary key (id_endereco, id_cliente)
 );
 select * from enderecos;

 create table cupom(
	cupom_desconto varchar(10) not null,
    desconto real(2,2) not null,
    primary key(cupom_desconto)
 );
 insert into cupom values ('NONE', 0.0);
 insert into cupom values ('DESC10', 0.9);
 insert into cupom values ('DESC5', 0.95);
 select * from cupom;

create table carrinho(
    id_carrinho int not null auto_increment,
	id_cliente int not null,
    cupom_desconto varchar(10) null,
	foreign key (id_cliente) references conta_cliente(id_cliente),
    foreign key (cupom_desconto) references cupom(cupom_desconto),
    primary key (id_carrinho)
);
select * from carrinho;

create table pedidos(
	id_pedido int not null auto_increment,
    id_endereco int null,
    status_pedido enum('não finalizado', 'confirmado', 'enviado', 'entregue') not null,
    data_pedido date null,
    id_carrinho int not null,
    valor_total real (6,2) not null,
    tipo_pgto enum('pix', 'boleto', 'cartao de credito') null,
    foreign key (id_endereco) references enderecos(id_endereco),
    foreign key (id_carrinho) references carrinho(id_carrinho),
    primary key (id_pedido)
);
select * from pedidos;

create table meses(
	num_mes int not null auto_increment,
    mes enum('janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro') not null,
	primary key (num_mes)
);

insert into meses(mes) values ('janeiro');
insert into meses(mes) values ('fevereiro');
insert into meses(mes) values ('marco');
insert into meses(mes) values ('abril');
insert into meses(mes) values ('maio');
insert into meses(mes) values ('junho');
insert into meses(mes) values ('julho');
insert into meses(mes) values ('agosto');
insert into meses(mes) values ('setembro');
insert into meses(mes) values ('outubro');
insert into meses(mes) values ('novembro');
insert into meses(mes) values ('dezembro');

create table produto(
	sku_produto int not null auto_increment,
    tipo_produto varchar(30) not null,
    quantidade integer(4) null,
    preco_produto real (4,2) not null,
    primary key (sku_produto)
);
select * from produto;

/*Todo item que é adicionado a um carrinho será adicionado à tabela itens_carrinho, caso contrário, constará apenas na quantidade de produtos disponíveis*/
create table itens_carrinho(
	id_item int not null auto_increment,
	sku_produto int not null,
    preco_compra real (4,2) not null,
    id_carrinho int not null,
    qtd_carrinho int not null,
    foreign key (sku_produto) references produto(sku_produto),
    foreign key (id_carrinho) references carrinho(id_carrinho),
    primary key (id_item)
);
select * from itens_carrinho;


