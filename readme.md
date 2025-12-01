# Compiler Toolkit

An opinionated library to help you build compilers.

# Features

- [ ] Ast Creation Tools
- [ ] Ast Walk functionality built in
- [ ] Ast node typing garauntees (ensure that all nodes are well defined)
- [ ] Ast nodes having configurable parser patterns
- [ ] Utility decorators for annotation of individual parts of the compilers
- [ ] Parser pattern builder
- [ ] Parser builder
- [ ] Parser check functions built into patterns to allow automatic syntax error parsing.
- [ ] Source error highlighting (fine grained highlights)
- [ ] Package and module tree utilities
- [ ] Lexing via rply library (and utilities)
- [ ] Parser token class builtin

# What this does not provide

- This will not do codegen
- This will not give you lexing capabilities outside of making the use of rply's lexer generator more ergonomic
- This will not provide a type system
- This will not teach you how to build a compiler (altho it will certainly aid in the creation of your first one!)
