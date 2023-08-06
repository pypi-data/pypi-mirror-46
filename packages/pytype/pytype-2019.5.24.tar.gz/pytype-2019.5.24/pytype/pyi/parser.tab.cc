// A Bison parser, made by GNU Bison 3.0.4.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Take the name prefix into account.
#define yylex   pytypelex

// First part of user declarations.

#line 39 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:404

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

#include "parser.tab.hh"

// User implementation prologue.

#line 53 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:412
// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:413

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 81 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:413


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (/*CONSTCOND*/ false)
# endif


// Suppress unused-variable warnings by "using" E.
#define YYUSE(E) ((void) (E))

// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << std::endl;                  \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE(Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void>(0)
# define YY_STACK_PRINT()                static_cast<void>(0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:479
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:479

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr = "";
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              // Fall through.
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if PYTYPEDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}


  /*---------------.
  | Symbol types.  |
  `---------------*/

  inline
  parser::syntax_error::syntax_error (const location_type& l, const std::string& m)
    : std::runtime_error (m)
    , location (l)
  {}

  // basic_symbol.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol ()
    : value ()
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& other)
    : Base (other)
    , value ()
    , location (other.location)
  {
    value = other.value;
  }


  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const semantic_type& v, const location_type& l)
    : Base (t)
    , value (v)
    , location (l)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  inline
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, const location_type& l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  inline
  parser::basic_symbol<Base>::~basic_symbol ()
  {
    clear ();
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::clear ()
  {
    Base::clear ();
  }

  template <typename Base>
  inline
  bool
  parser::basic_symbol<Base>::empty () const
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  inline
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move(s);
    value = s.value;
    location = s.location;
  }

  // by_type.
  inline
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

  inline
  parser::by_type::by_type (const by_type& other)
    : type (other.type)
  {}

  inline
  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  inline
  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  inline
  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  inline
  int
  parser::by_type::type_get () const
  {
    return type;
  }


  // by_state.
  inline
  parser::by_state::by_state ()
    : state (empty_state)
  {}

  inline
  parser::by_state::by_state (const by_state& other)
    : state (other.state)
  {}

  inline
  void
  parser::by_state::clear ()
  {
    state = empty_state;
  }

  inline
  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  inline
  parser::by_state::by_state (state_type s)
    : state (s)
  {}

  inline
  parser::symbol_number_type
  parser::by_state::type_get () const
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  inline
  parser::stack_symbol_type::stack_symbol_type ()
  {}


  inline
  parser::stack_symbol_type::stack_symbol_type (state_type s, symbol_type& that)
    : super_type (s, that.location)
  {
    value = that.value;
    // that is emptied.
    that.type = empty_symbol;
  }

  inline
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }


  template <typename Base>
  inline
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
            case 3: // NAME

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 4: // NUMBER

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 5: // LEXERROR

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 48: // start

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 442 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 49: // unit

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 449 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 50: // alldefs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 52: // classdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 463 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 53: // class_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 54: // parents

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 477 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 55: // parent_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 56: // parent

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 57: // maybe_class_funcs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 58: // class_funcs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 505 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 59: // funcdefs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 60: // if_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 519 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 61: // if_and_elifs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 62: // class_if_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 63: // class_if_and_elifs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 540 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 64: // if_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 547 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 65: // elif_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 66: // else_cond

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 67: // condition

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 68: // version_tuple

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 575 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 69: // condition_op

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.str)); }
#line 582 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 70: // constantdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 71: // importdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 72: // import_items

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 603 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 73: // import_item

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 610 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 74: // import_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 617 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 75: // from_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 76: // from_items

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 631 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 77: // from_item

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 78: // alias_or_constant

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 645 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 79: // typevardef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 80: // typevar_args

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 81: // typevar_kwargs

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 82: // typevar_kwarg

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 673 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 83: // funcdef

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 84: // funcname

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 85: // decorators

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 86: // decorator

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 87: // params

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 88: // param_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 715 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 89: // param

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 90: // param_type

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 729 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 91: // param_default

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 92: // param_star_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 743 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 93: // return

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 750 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 95: // maybe_body

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 97: // body

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 98: // body_stmt

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 99: // type_parameters

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 100: // type_parameter

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 785 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 101: // type

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 792 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 102: // named_tuple_fields

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 799 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 103: // named_tuple_field_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 104: // named_tuple_field

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 813 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 106: // coll_named_tuple_fields

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 107: // coll_named_tuple_field_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 108: // coll_named_tuple_field

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 834 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 109: // maybe_type_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 841 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 110: // type_list

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 848 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 111: // type_tuple_elements

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 855 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 112: // type_tuple_literal

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 113: // dotted_name

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 869 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 114: // getitem_key

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 876 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;

      case 115: // maybe_number

#line 100 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:614
        { Py_CLEAR((yysym.value.obj)); }
#line 883 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:614
        break;


      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  inline
  void
  parser::yypush_ (const char* m, state_type s, symbol_type& sym)
  {
    stack_symbol_type t (s, sym);
    yypush_ (m, t);
  }

  inline
  void
  parser::yypush_ (const char* m, stack_symbol_type& s)
  {
    if (m)
      YY_SYMBOL_PRINT (m, s);
    yystack_.push (s);
  }

  inline
  void
  parser::yypop_ (unsigned int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  inline parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  inline bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  inline bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

    // FIXME: This shoud be completely indented.  It is not yet to
    // avoid gratuitous conflicts when merging into the master branch.
    try
      {
    YYCDEBUG << "Starting parse" << std::endl;


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, yyla);

    // A new symbol was pushed on the stack.
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << std::endl;

    // Accept?
    if (yystack_[0].state == yyfinal_)
      goto yyacceptlab;

    goto yybackup;

    // Backup.
  yybackup:

    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
        try
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
        catch (const syntax_error& yyexc)
          {
            error (yyexc);
            goto yyerrlab1;
          }
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, yyla);
    goto yynewstate;

  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;

  /*-----------------------------.
  | yyreduce -- Do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_(yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Compute the default @$.
      {
        slice<stack_symbol_type, stack_type> slice (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, slice, yylen);
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
      try
        {
          switch (yyn)
            {
  case 2:
#line 133 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1122 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 3:
#line 134 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1128 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 5:
#line 142 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1134 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 6:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1140 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 7:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1146 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 8:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1157 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 9:
#line 151 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1163 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 10:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 11:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1179 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 12:
#line 158 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1185 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 15:
#line 169 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNN)", (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1194 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 16:
#line 176 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1207 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 17:
#line 187 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1213 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 18:
#line 188 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1219 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 19:
#line 189 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1225 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 20:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1231 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 21:
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1237 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 22:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1243 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 23:
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1249 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 24:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1255 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 25:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1261 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 26:
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1267 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 27:
#line 209 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1273 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 29:
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1279 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 30:
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1289 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 31:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1295 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 32:
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1305 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 33:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1311 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 34:
#line 227 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1317 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 35:
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1325 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 37:
#line 240 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1333 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 38:
#line 244 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1341 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 39:
#line 263 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1349 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 41:
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 42:
#line 275 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1365 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 43:
#line 287 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1371 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 44:
#line 291 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1377 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 45:
#line 295 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1383 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 46:
#line 299 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1391 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 47:
#line 302 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 48:
#line 305 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1407 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 49:
#line 308 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1415 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 50:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 51:
#line 312 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1427 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 52:
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1433 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 53:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1439 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 54:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1445 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 55:
#line 320 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1453 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 56:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<"; }
#line 1459 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 57:
#line 327 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">"; }
#line 1465 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 58:
#line 328 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "<="; }
#line 1471 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 59:
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = ">="; }
#line 1477 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 60:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "=="; }
#line 1483 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 61:
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.str) = "!="; }
#line 1489 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 62:
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 63:
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kByteString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1507 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 64:
#line 343 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kUnicodeString));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1516 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 65:
#line 347 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1525 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 66:
#line 351 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1534 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 67:
#line 355 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1543 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 68:
#line 359 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1552 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 69:
#line 363 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 70:
#line 370 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1570 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 71:
#line 374 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1579 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 72:
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 73:
#line 384 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1601 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 74:
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 75:
#line 394 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1613 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 77:
#line 398 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1619 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 79:
#line 404 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1628 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 81:
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1634 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 82:
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1640 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 83:
#line 417 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1646 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 84:
#line 418 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 86:
#line 423 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1660 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 87:
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 88:
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1676 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 89:
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1684 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 90:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1690 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 91:
#line 439 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1696 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 92:
#line 443 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1705 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 93:
#line 450 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1711 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 94:
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1717 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 95:
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1723 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 96:
#line 453 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1729 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 97:
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1735 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 98:
#line 458 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1741 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 99:
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1747 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 100:
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NNNNN)", (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1766 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 101:
#line 483 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1772 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 102:
#line 484 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 103:
#line 488 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1784 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 104:
#line 489 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1790 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 105:
#line 493 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1796 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 106:
#line 497 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1802 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 107:
#line 498 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 108:
#line 510 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 109:
#line 511 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 110:
#line 515 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 111:
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 112:
#line 517 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1838 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 113:
#line 518 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1844 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 114:
#line 522 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1850 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 115:
#line 523 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1856 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 116:
#line 527 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 117:
#line 528 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1868 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 118:
#line 529 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1874 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 119:
#line 530 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1880 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 120:
#line 534 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1886 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 121:
#line 535 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1892 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 122:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1898 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 123:
#line 540 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1904 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 124:
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1910 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 125:
#line 548 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1916 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 126:
#line 549 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1922 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 127:
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 1928 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 135:
#line 564 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1934 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 136:
#line 565 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1940 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 137:
#line 569 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1946 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 138:
#line 570 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1952 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 139:
#line 571 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1958 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 140:
#line 575 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1964 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 141:
#line 576 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1970 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 142:
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1976 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 143:
#line 581 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1982 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 144:
#line 585 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1991 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 145:
#line 589 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2000 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 146:
#line 593 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      // This rule is needed for Callable[[...], ...]
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2010 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 147:
#line 598 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2019 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 148:
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2028 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 149:
#line 606 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2034 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 150:
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2040 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 151:
#line 608 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2046 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 152:
#line 609 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2052 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 153:
#line 610 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2058 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 154:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2064 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 155:
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2070 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 156:
#line 619 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2076 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 157:
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2082 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 158:
#line 624 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2088 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 161:
#line 633 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2094 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 162:
#line 634 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2100 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 163:
#line 638 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2108 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 164:
#line 641 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2114 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 165:
#line 645 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2120 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 166:
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2126 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 167:
#line 649 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = PyList_New(0); }
#line 2132 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 168:
#line 653 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2138 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 169:
#line 654 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 170:
#line 661 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2150 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 171:
#line 662 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2156 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 172:
#line 671 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2165 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 173:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2174 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 174:
#line 682 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2183 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 175:
#line 689 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2189 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 176:
#line 690 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2205 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 177:
#line 704 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2211 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 178:
#line 705 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2221 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 179:
#line 710 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2231 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 180:
#line 718 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2237 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;

  case 181:
#line 719 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:859
    { (yylhs.value.obj) = NULL; }
#line 2243 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
    break;


#line 2247 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:859
            default:
              break;
            }
        }
      catch (const syntax_error& yyexc)
        {
          error (yyexc);
          YYERROR;
        }
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, yylhs);
    }
    goto yynewstate;

  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:

    /* Pacify compilers like GCC when the user code never invokes
       YYERROR and the label yyerrorlab therefore never appears in user
       code.  */
    if (false)
      goto yyerrorlab;
    yyerror_range[1].location = yystack_[yylen - 1].location;
    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;

  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", error_token);
    }
    goto yynewstate;

    // Accept.
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;

    // Abort.
  yyabortlab:
    yyresult = 1;
    goto yyreturn;

  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack"
                 << std::endl;
        // Do not try to display the values of the reclaimed symbols,
        // as their printer might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
        YYCASE_(0, YY_("syntax error"));
        YYCASE_(1, YY_("syntax error, unexpected %s"));
        YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short int parser::yypact_ninf_ = -229;

  const short int parser::yytable_ninf_ = -181;

  const short int
  parser::yypact_[] =
  {
       2,  -229,   112,   156,   360,   194,  -229,  -229,    60,   143,
      84,   216,     9,  -229,  -229,   221,   218,  -229,  -229,  -229,
    -229,  -229,    41,  -229,   163,   129,  -229,   207,  -229,    84,
     246,   313,   100,  -229,     4,    37,   253,   226,  -229,    84,
     240,   242,   255,    19,   216,  -229,  -229,   263,   271,   163,
     163,  -229,   234,   285,  -229,   276,   287,  -229,  -229,   163,
     173,  -229,   160,   257,   179,    84,    84,  -229,  -229,  -229,
    -229,   323,  -229,  -229,   318,    86,   329,   216,  -229,  -229,
     350,   229,    81,  -229,   229,   246,   336,   341,  -229,  -229,
    -229,   338,    62,   369,   374,   298,   337,   339,   343,   163,
     163,   355,  -229,    26,   378,   163,   283,   345,  -229,   346,
    -229,   309,  -229,   337,   352,  -229,   373,  -229,   353,   349,
     354,  -229,  -229,   382,  -229,  -229,  -229,  -229,   375,  -229,
    -229,  -229,    47,  -229,   352,   356,  -229,   229,    13,   352,
    -229,  -229,   256,    20,  -229,   357,   358,  -229,  -229,   163,
     380,  -229,   352,  -229,   114,  -229,   337,   359,   305,   185,
     163,   361,   163,  -229,   198,   184,   317,   386,   362,   395,
     314,  -229,    47,   352,  -229,   272,   278,  -229,   366,  -229,
      27,   365,   367,  -229,   366,   363,   364,   337,  -229,    26,
    -229,   208,   370,  -229,  -229,   337,   337,  -229,   337,  -229,
    -229,  -229,   146,  -229,   352,    99,  -229,   371,    92,  -229,
    -229,    34,  -229,  -229,  -229,  -229,   163,   372,  -229,   404,
     387,    -3,  -229,  -229,   104,   376,    89,   377,  -229,   379,
     381,  -229,   383,  -229,     1,   385,   250,  -229,  -229,  -229,
    -229,   386,   331,  -229,  -229,   337,   310,  -229,  -229,   163,
     388,    20,   405,  -229,   384,  -229,  -229,  -229,  -229,   389,
    -229,  -229,   163,   408,   208,   390,  -229,   292,  -229,  -229,
     221,   391,  -229,  -229,  -229,  -229,  -229,   411,  -229,  -229,
    -229,   337,   334,  -229,  -229,  -229,   392,   393,   394,   413,
     396,   337,   379,  -229,   381,  -229,   154,   397,   398,   399,
     401,   238,   348,   352,   163,  -229,  -229,  -229,  -229,   402,
     407,  -229,  -229,   400,   163,   410,   205,  -229,   412,   312,
    -229,  -229,   202,  -229,  -229,   293,   163,     7,  -229,  -229,
    -229,  -229,   260,   414,  -229,   406,   294,   302,  -229,   337,
     409,  -229,  -229,  -229,  -229,  -229,  -229
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   104,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    36,     0,     5,     7,     8,
      10,     6,     0,     3,     0,     0,    16,    19,   175,     0,
      43,     0,    14,    75,    76,     0,     0,    78,    45,     0,
       0,     0,     0,     0,     0,   103,   153,     0,     0,     0,
     167,   152,    14,   144,    62,     0,    66,    63,    64,     0,
      91,    65,     0,     0,     0,     0,     0,    60,    61,    58,
      59,   181,    56,    57,     0,     0,     0,     0,    70,    13,
       0,     0,     0,    79,     0,    44,     0,     0,    12,   101,
     102,     0,    14,     0,     0,     0,   169,     0,   166,     0,
       0,     0,    68,     0,     0,     0,     0,   160,   174,   175,
      18,     0,    21,    22,    14,    52,    51,    50,   177,     0,
       0,   176,    46,     0,    47,   124,    74,    77,    85,    86,
      87,    88,     0,    89,    14,    80,    84,     0,     0,    14,
      12,    12,   104,   107,   105,     0,     0,   149,   146,     0,
     151,   150,    14,   143,     0,   141,   142,    93,    14,     0,
     159,     0,     0,    17,     0,     0,     0,   181,     0,     0,
       0,    72,     0,    14,    71,   104,   104,    37,   115,   113,
     111,     0,   160,   109,   115,     0,     0,   168,    69,     0,
     145,     0,     0,    67,   173,   171,   170,   172,    23,    20,
     182,   183,    34,    15,    14,     0,   180,   178,     0,    90,
      81,     0,    83,    73,    38,    35,     0,   119,   120,     0,
     123,    14,   106,   112,     0,     0,     0,     0,   140,   175,
      95,    98,    94,    92,    34,     0,   104,    27,    24,    48,
      49,   181,     0,    53,    82,   114,     0,   110,   121,     0,
     134,     0,     0,   155,   160,   157,   147,   165,   162,   160,
     164,   148,     0,     0,     0,     0,    25,     0,    33,    32,
      40,     0,    29,    30,    31,   179,    54,     0,   116,   117,
     118,   122,     0,   100,   127,   108,     0,   159,     0,   159,
       0,    99,     0,    97,    96,    26,     0,     0,     0,     0,
       0,     0,     0,   128,     0,   156,   154,   163,   161,     0,
       0,    34,    55,     0,     0,     0,     0,   136,     0,     0,
     130,   129,   160,    34,    34,   104,     0,   138,   133,   126,
     135,   132,     0,     0,   159,     0,   104,   104,    41,   137,
       0,   125,   131,   158,    42,    39,   139
  };

  const short int
  parser::yypgoto_[] =
  {
    -229,  -229,   422,   -81,   -51,  -228,  -229,  -229,  -229,   269,
    -229,   190,   -88,  -229,  -229,  -229,  -229,  -226,   170,   174,
      61,   241,   281,  -223,  -229,  -229,   403,   436,   -75,   319,
    -138,  -221,  -229,  -229,   186,   189,  -219,  -229,  -229,  -229,
    -229,  -229,   203,   265,  -229,  -229,  -229,  -162,  -229,  -229,
     134,  -161,  -229,   266,   -24,  -229,  -229,   169,  -177,  -229,
    -229,   168,  -229,   267,  -229,  -229,    -8,  -229,  -156,  -159
  };

  const short int
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    78,    13,    27,    63,   111,   112,
     203,   235,   236,    14,    15,   269,   270,    16,    40,    41,
      30,   124,    75,    17,    18,    32,    33,    83,   134,   135,
     136,    19,    20,   192,   230,   231,    21,    91,    22,    45,
     181,   182,   183,   217,   247,   184,   250,    79,   283,   284,
     316,   317,   154,   155,    60,   225,   254,   255,   161,   227,
     259,   260,    97,    98,   107,    61,    53,   119,   120,   237
  };

  const short int
  parser::yytable_[] =
  {
      52,   102,    31,    34,    37,   222,   204,   142,   268,   139,
     271,   207,    28,   272,   200,   273,    28,   274,    99,   100,
      80,    31,    89,   178,   201,    95,    96,    37,    76,    28,
     218,    31,     1,  -159,   212,   106,    92,   128,   113,    90,
      28,   144,   340,   179,    46,    47,    48,    74,    43,   153,
     128,    81,    35,   129,   130,   131,   138,    31,    31,   175,
     176,    49,   173,   165,   180,    50,   129,   130,   131,    34,
     244,   219,    51,   212,    37,   150,   151,   288,   133,   156,
      82,   158,   290,   171,    28,   275,    44,    28,   174,   122,
      64,   133,   257,    76,    24,   137,   242,   268,    25,   271,
      85,   188,   272,   239,   273,    74,   274,   193,   268,   268,
     271,   271,     6,   272,   272,   273,   273,   274,   274,    29,
     302,   123,   213,   303,   138,   187,   116,   117,   243,   258,
      37,    76,    28,    54,   123,   195,   196,    77,   198,   252,
     113,   321,   318,   320,   253,   335,    26,    46,    47,    48,
      55,   189,    56,   238,   190,   330,     7,    28,    54,   200,
     333,    57,    58,   109,    59,   156,    28,    96,    50,   201,
     251,   330,    46,    47,    48,    51,   234,    56,    46,    47,
      48,    46,    47,    48,    99,   100,    57,    58,    28,    59,
      65,    66,   245,    50,    23,    49,   110,   200,    49,    50,
      51,   109,    50,    46,    47,    48,    51,   201,   313,    51,
     108,   229,   202,    99,   100,   115,    46,    47,    48,    28,
      49,   194,   314,   325,    50,   281,    46,    47,    48,    38,
      39,    51,   128,    49,   329,   336,   337,    50,   291,   334,
     187,   313,    62,    49,    51,    99,   100,    50,   129,   130,
     131,   200,    42,   267,    51,   314,     9,    65,    66,     8,
      10,   201,     9,   313,   132,    76,    10,    84,   315,    74,
      11,    12,   101,   133,    86,     8,    87,   314,     9,   -28,
     322,     8,    10,    88,     9,   177,    11,    12,    10,   341,
     327,   114,    11,    12,    99,   100,   267,   267,    93,     9,
       9,   214,   339,    10,    10,   267,    94,   215,     9,    99,
     100,   104,    10,   278,   279,   313,    99,   100,   105,   147,
     159,   121,   338,   344,   103,   200,    24,   118,    74,   314,
     296,   345,   125,   280,   147,   201,    76,    67,    68,    69,
      70,    67,    68,    69,    70,   163,   164,   200,    99,   100,
     210,   211,    71,   127,    72,    73,    74,   201,    72,    73,
      -4,   200,   301,     8,   140,    76,     9,   276,   277,   141,
      10,   201,   145,   143,    11,    12,   319,   146,   152,   148,
     149,   157,   160,    76,   162,    66,   168,  -180,   167,   166,
     206,   169,   100,   172,   185,   186,   191,   197,   209,   208,
     216,   220,   224,   226,   221,   241,   233,   248,   286,   249,
     246,   292,   256,   261,   266,   300,   257,   262,   263,   295,
     264,   287,   282,     5,   265,   299,   289,   311,   252,   304,
     323,   309,   310,   199,   306,   324,   308,   312,   326,   328,
     297,   331,   343,   342,   298,   346,   240,   205,    36,   223,
     294,   170,   293,   332,   285,   228,   305,   307,   232,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     126
  };

  const short int
  parser::yycheck_[] =
  {
      24,    52,    10,    11,    12,   182,   165,    88,   236,    84,
     236,   167,     3,   236,    13,   236,     3,   236,    11,    12,
      16,    29,     3,     3,    23,    49,    50,    35,    31,     3,
       3,    39,    30,    36,   172,    59,    44,     3,    62,    20,
       3,    92,    35,    23,    18,    19,    20,    43,     7,    23,
       3,    14,    43,    19,    20,    21,    43,    65,    66,   140,
     141,    35,   137,   114,    44,    39,    19,    20,    21,    77,
      36,    44,    46,   211,    82,    99,   100,   254,    44,   103,
      43,   105,   259,   134,     3,   241,    45,     3,   139,     3,
      29,    44,     3,    31,    34,    14,     4,   325,    38,   325,
      39,   152,   325,     4,   325,    43,   325,   158,   336,   337,
     336,   337,     0,   336,   337,   336,   337,   336,   337,    35,
     282,    35,   173,   282,    43,   149,    65,    66,    36,    40,
     138,    31,     3,     4,    35,   159,   160,    37,   162,    35,
     164,   303,   301,   302,    40,   322,     3,    18,    19,    20,
      21,    37,    23,   204,    40,   316,     0,     3,     4,    13,
     319,    32,    33,     3,    35,   189,     3,   191,    39,    23,
     221,   332,    18,    19,    20,    46,    30,    23,    18,    19,
      20,    18,    19,    20,    11,    12,    32,    33,     3,    35,
      11,    12,   216,    39,     0,    35,    36,    13,    35,    39,
      46,     3,    39,    18,    19,    20,    46,    23,     3,    46,
      37,     3,    28,    11,    12,    36,    18,    19,    20,     3,
      35,    36,    17,   311,    39,   249,    18,    19,    20,     8,
       9,    46,     3,    35,    29,   323,   324,    39,   262,    37,
     264,     3,    35,    35,    46,    11,    12,    39,    19,    20,
      21,    13,    34,     3,    46,    17,     6,    11,    12,     3,
      10,    23,     6,     3,    35,    31,    10,    14,    30,    43,
      14,    15,    38,    44,    34,     3,    34,    17,     6,    29,
     304,     3,    10,    28,     6,    29,    14,    15,    10,    29,
     314,    34,    14,    15,    11,    12,     3,     3,    35,     6,
       6,    29,   326,    10,    10,     3,    35,    29,     6,    11,
      12,    35,    10,     3,     4,     3,    11,    12,    31,    36,
      37,     3,    29,    29,    39,    13,    34,     4,    43,    17,
      38,    29,     3,    23,    36,    23,    31,    24,    25,    26,
      27,    24,    25,    26,    27,    36,    37,    13,    11,    12,
      36,    37,    39,     3,    41,    42,    43,    23,    41,    42,
       0,    13,    28,     3,    28,    31,     6,    36,    37,    28,
      10,    23,     3,    35,    14,    15,    28,     3,    23,    40,
      37,     3,    37,    31,    38,    12,     4,    34,    34,    40,
       4,    16,    12,    37,    37,    37,    37,    36,     3,    37,
      34,    36,    39,    39,    37,    34,    36,     3,     3,    22,
      38,     3,    36,    36,    29,     4,     3,    38,    37,    29,
      37,    37,    34,     1,   234,    34,    37,    28,    35,    37,
      28,    34,    34,   164,    40,    28,    40,    36,    38,    29,
     270,    29,    36,    29,   270,    36,   205,   166,    12,   184,
     264,   132,   263,   319,   251,   189,   287,   289,   191,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      77
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    30,    48,    49,    50,    49,     0,     0,     3,     6,
      10,    14,    15,    52,    60,    61,    64,    70,    71,    78,
      79,    83,    85,     0,    34,    38,     3,    53,     3,    35,
      67,   113,    72,    73,   113,    43,    74,   113,     8,     9,
      65,    66,    34,     7,    45,    86,    18,    19,    20,    35,
      39,    46,   101,   113,     4,    21,    23,    32,    33,    35,
     101,   112,    35,    54,    67,    11,    12,    24,    25,    26,
      27,    39,    41,    42,    43,    69,    31,    37,    51,    94,
      16,    14,    43,    74,    14,    67,    34,    34,    28,     3,
      20,    84,   113,    35,    35,   101,   101,   109,   110,    11,
      12,    38,    51,    39,    35,    31,   101,   111,    37,     3,
      36,    55,    56,   101,    34,    36,    67,    67,     4,   114,
     115,     3,     3,    35,    68,     3,    73,     3,     3,    19,
      20,    21,    35,    44,    75,    76,    77,    14,    43,    75,
      28,    28,    50,    35,    51,     3,     3,    36,    40,    37,
     101,   101,    23,    23,    99,   100,   101,     3,   101,    37,
      37,   105,    38,    36,    37,    51,    40,    34,     4,    16,
      76,    51,    37,    75,    51,    50,    50,    29,     3,    23,
      44,    87,    88,    89,    92,    37,    37,   101,    51,    37,
      40,    37,    80,    51,    36,   101,   101,    36,   101,    56,
      13,    23,    28,    57,   116,    69,     4,   115,    37,     3,
      36,    37,    77,    51,    29,    29,    34,    90,     3,    44,
      36,    37,   105,    90,    39,   102,    39,   106,   100,     3,
      81,    82,   110,    36,    30,    58,    59,   116,    51,     4,
      68,    34,     4,    36,    36,   101,    38,    91,     3,    22,
      93,    51,    35,    40,   103,   104,    36,     3,    40,   107,
     108,    36,    38,    37,    37,    58,    29,     3,    52,    62,
      63,    64,    70,    78,    83,   115,    36,    37,     3,     4,
      23,   101,    34,    95,    96,    89,     3,    37,   105,    37,
     105,   101,     3,    82,    81,    29,    38,    65,    66,    34,
       4,    28,    94,   116,    37,   104,    40,   108,    40,    34,
      34,    28,    36,     3,    17,    30,    97,    98,   116,    28,
     116,    94,   101,    28,    28,    59,    38,   101,    29,    29,
      98,    29,    97,   116,    37,   105,    59,    59,    29,   101,
      35,    29,    29,    36,    29,    29,    36
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    47,    48,    48,    49,    50,    50,    50,    50,    50,
      50,    50,    50,    51,    51,    52,    53,    54,    54,    54,
      55,    55,    56,    56,    57,    57,    57,    58,    58,    59,
      59,    59,    59,    59,    59,    60,    60,    61,    61,    62,
      62,    63,    63,    64,    65,    66,    67,    67,    67,    67,
      67,    67,    67,    68,    68,    68,    69,    69,    69,    69,
      69,    69,    70,    70,    70,    70,    70,    70,    70,    70,
      71,    71,    71,    71,    72,    72,    73,    73,    74,    74,
      75,    75,    75,    76,    76,    77,    77,    77,    77,    77,
      77,    78,    79,    80,    80,    80,    80,    81,    81,    82,
      83,    84,    84,    85,    85,    86,    87,    87,    88,    88,
      89,    89,    89,    89,    90,    90,    91,    91,    91,    91,
      92,    92,    93,    93,    94,    95,    95,    95,    96,    96,
      96,    96,    96,    96,    96,    97,    97,    98,    98,    98,
      99,    99,   100,   100,   101,   101,   101,   101,   101,   101,
     101,   101,   101,   101,   102,   102,   103,   103,   104,   105,
     105,   106,   106,   107,   107,   108,   109,   109,   110,   110,
     111,   111,   112,   112,   112,   113,   113,   114,   114,   114,
     115,   115,   116,   116
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     6,     1,     3,     2,     0,
       3,     1,     1,     3,     2,     3,     4,     1,     1,     2,
       2,     2,     2,     2,     0,     6,     1,     5,     6,     6,
       1,     5,     6,     2,     2,     1,     3,     3,     6,     6,
       3,     3,     3,     4,     5,     7,     1,     1,     1,     1,
       1,     1,     3,     3,     3,     3,     3,     6,     4,     6,
       3,     5,     5,     6,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     1,
       3,     3,     7,     0,     2,     2,     4,     3,     1,     3,
       8,     1,     1,     2,     0,     3,     2,     0,     4,     1,
       3,     1,     2,     1,     2,     0,     2,     2,     2,     0,
       2,     3,     2,     0,     2,     5,     4,     1,     2,     3,
       3,     5,     4,     4,     0,     2,     1,     3,     2,     4,
       3,     1,     1,     1,     1,     4,     3,     6,     6,     3,
       3,     3,     1,     1,     4,     2,     3,     1,     6,     1,
       0,     4,     2,     3,     1,     1,     1,     0,     3,     1,
       3,     3,     4,     4,     2,     1,     3,     1,     3,     5,
       1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "LEXERROR",
  "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND", "PASS", "IMPORT",
  "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE", "COLL_NAMEDTUPLE",
  "TYPEVAR", "ARROW", "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT",
  "DEDENT", "TRIPLEQUOTED", "TYPECOMMENT", "BYTESTRING", "UNICODESTRING",
  "':'", "'('", "')'", "','", "'='", "'['", "']'", "'<'", "'>'", "'.'",
  "'*'", "'@'", "'?'", "$accept", "start", "unit", "alldefs",
  "maybe_type_ignore", "classdef", "class_name", "parents", "parent_list",
  "parent", "maybe_class_funcs", "class_funcs", "funcdefs", "if_stmt",
  "if_and_elifs", "class_if_stmt", "class_if_and_elifs", "if_cond",
  "elif_cond", "else_cond", "condition", "version_tuple", "condition_op",
  "constantdef", "importdef", "import_items", "import_item", "import_name",
  "from_list", "from_items", "from_item", "alias_or_constant",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "params", "param_list",
  "param", "param_type", "param_default", "param_star_name", "return",
  "typeignore", "maybe_body", "empty_body", "body", "body_stmt",
  "type_parameters", "type_parameter", "type", "named_tuple_fields",
  "named_tuple_field_list", "named_tuple_field", "maybe_comma",
  "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "maybe_type_list", "type_list",
  "type_tuple_elements", "type_tuple_literal", "dotted_name",
  "getitem_key", "maybe_number", "pass_or_ellipsis", YY_NULLPTR
  };

#if PYTYPEDEBUG
  const unsigned short int
  parser::yyrline_[] =
  {
       0,   133,   133,   134,   138,   142,   143,   144,   145,   151,
     152,   153,   158,   162,   163,   169,   176,   187,   188,   189,
     193,   194,   198,   199,   203,   204,   205,   209,   210,   214,
     215,   220,   221,   226,   227,   232,   235,   240,   244,   263,
     266,   271,   275,   287,   291,   295,   299,   302,   305,   308,
     311,   312,   313,   318,   319,   320,   326,   327,   328,   329,
     330,   331,   335,   339,   343,   347,   351,   355,   359,   363,
     370,   374,   378,   384,   393,   394,   397,   398,   403,   404,
     411,   412,   413,   417,   418,   422,   423,   426,   429,   432,
     435,   439,   443,   450,   451,   452,   453,   457,   458,   462,
     466,   483,   484,   488,   489,   493,   497,   498,   510,   511,
     515,   516,   517,   518,   522,   523,   527,   528,   529,   530,
     534,   535,   539,   540,   544,   548,   549,   550,   554,   555,
     556,   557,   558,   559,   560,   564,   565,   569,   570,   571,
     575,   576,   580,   581,   585,   589,   593,   598,   602,   606,
     607,   608,   609,   610,   614,   615,   619,   620,   624,   628,
     629,   633,   634,   638,   641,   645,   648,   649,   653,   654,
     661,   662,   671,   676,   682,   689,   690,   704,   705,   710,
     718,   719,   723,   724
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << std::endl;
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):" << std::endl;
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  // Symbol number corresponding to token number t.
  inline
  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    static
    const token_number_type
    translate_table[] =
    {
     0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      35,    36,    44,     2,    37,     2,    43,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    34,     2,
      41,    38,    42,    46,    45,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    39,     2,    40,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33
    };
    const unsigned int user_token_number_max_ = 288;
    const token_number_type undef_token_ = 2;

    if (static_cast<int>(t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned int> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1167
} // pytype
#line 2944 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc" // lalr1.cc:1167
#line 727 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy" // lalr1.cc:1168


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
