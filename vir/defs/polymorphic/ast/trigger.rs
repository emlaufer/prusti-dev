// © 2019, ETH Zurich
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

use crate::polymorphic::ast::*;
use std::{collections::HashMap, fmt};

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Trigger(pub(crate) Vec<Expr>);

impl fmt::Display for Trigger {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{{{}}}",
            self.0
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<String>>()
                .join(", ")
        )
    }
}

impl Trigger {
    pub fn new(items: Vec<Expr>) -> Self {
        Trigger(items)
    }

    pub fn elements(&self) -> &Vec<Expr> {
        &self.0
    }

    // TODO polymorphic: potentially remove usage of these 2 functions
    pub fn replace_place(self, target: &Expr, replacement: &Expr) -> Self {
        Trigger(
            self.0
                .into_iter()
                .map(|x| x.replace_place(target, replacement))
                .collect(),
        )
    }

    pub fn replace_multiple_places(self, replacements: &[(Expr, Expr)]) -> Self {
        Trigger(
            self.0
                .into_iter()
                .map(|x| x.replace_multiple_places(replacements))
                .collect(),
        )
    }
}
