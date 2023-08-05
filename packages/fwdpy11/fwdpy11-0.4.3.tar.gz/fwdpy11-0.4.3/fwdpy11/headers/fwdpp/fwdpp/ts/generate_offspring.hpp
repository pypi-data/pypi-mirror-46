#ifndef FWDPP_TS_GENERATE_OFFSPRING_HPP
#define FWDPP_TS_GENERATE_OFFSPRING_HPP

#include <stdexcept>
#include <tuple>
#include <vector>
#include <utility>
#include <type_traits>
#include <gsl/gsl_rng.h>
#include <fwdpp/debug.hpp>
#include <fwdpp/wrapped_range.hpp>
#include <fwdpp/forward_types.hpp>
#include <fwdpp/mutate_recombine.hpp>
#include <fwdpp/internal/mutation_internal.hpp>

namespace fwdpp
{
    namespace ts
    {
        struct mut_rec_intermediates
        /// Contains the output of recombination and mutation when generating offspring gametes.
        /// Objects of this type are returned by fwdpp::ts::generate_offspring.
        /// \version 0.7.4 Added to fwdpp::ts.
        {
            /// 1 if the parent gametes were swapped, 0 otherwise
            int swapped;
            /// Recombination breakpoints
            std::vector<double> breakpoints;
            /// Keys to new mutations
            std::vector<uint_t> mutation_keys;

            template <typename B, typename M>
            mut_rec_intermediates(int s, B&& b, M&& m)
                : swapped{ s }, breakpoints{ std::forward<B>(b) },
                  mutation_keys{ std::forward<M>(m) }
            {
            }
        };

        struct all_mutations
        /// Dispatch tag. See docs for fwdpp::ts::generate_offspring
        /// \version 0.7.4 Added to fwdpp::ts.
        {
        };

        struct selected_variants_only
        /// Dispatch tag. See docs for fwdpp::ts::generate_offspring
        /// \version 0.7.4 Added to fwdpp::ts.
        {
        };

        namespace detail
        {

            template <typename key_vector, typename mcont_t>
            inline wrapped_range<typename key_vector::iterator>
            process_new_mutations(const key_vector& new_mutation_keys,
                                  const mcont_t&, all_mutations)
            {
                return make_wrapped_range(begin(new_mutation_keys),
                                          end(new_mutation_keys));
            }

            template <typename key_vector, typename mcont_t>
            inline wrapped_range<typename key_vector::iterator>
            process_new_mutations(key_vector& new_mutation_keys,
                                  mcont_t& mutations, selected_variants_only)
            {
                auto itr = std::stable_partition(
                    begin(new_mutation_keys), end(new_mutation_keys),
                    [&mutations](typename key_vector::value_type k) {
                        return mutations[k].neutral == false;
                    });
                return make_wrapped_range(begin(new_mutation_keys), itr);
            }

            template <typename poptype, typename recmodel, typename mutmodel>
            inline mut_rec_intermediates
            generate_mutations_and_breakpoints(
                std::size_t parent, std::size_t parental_gamete, int swapped,
                const recmodel& generate_breakpoints,
                const mutmodel& generate_mutations,
                flagged_mutation_queue& mutation_recycling_bin, poptype& pop)
            {
                auto breakpoints = generate_breakpoints();
                auto new_mutation_keys = fwdpp_internal::mmodel_dispatcher(
                    generate_mutations, pop.diploids[parent],
                    pop.gametes[parental_gamete], pop.mutations,
                    mutation_recycling_bin);
                return mut_rec_intermediates(swapped, std::move(breakpoints),
                                             std::move(new_mutation_keys));
            }

            struct parental_data
            {
                std::size_t index, gamete1, gamete2;
                int swapped;
            };

            template <typename poptype, typename recmodel, typename mutmodel,
                      typename mutation_key_container,
                      typename mutation_handling_policy>
            inline std::pair<std::size_t, mut_rec_intermediates>
            generate_offspring_gamete(
                const parental_data parent,
                const recmodel& generate_breakpoints,
                const mutmodel& generate_mutations,
                const mutation_handling_policy& mutation_policy,
                flagged_mutation_queue& mutation_recycling_bin,
                flagged_gamete_queue& gamete_recycling_bin,
                mutation_key_container& neutral,
                mutation_key_container& selected, poptype& pop)
            {
                auto gamete_data = generate_mutations_and_breakpoints(
                    parent.index, parent.gamete1, parent.swapped,
                    generate_breakpoints, generate_mutations,
                    mutation_recycling_bin, pop);
                auto range = process_new_mutations(
                    gamete_data.mutation_keys, pop.mutations, mutation_policy);
                std::size_t offspring_gamete = mutate_recombine(
                    range, gamete_data.breakpoints, parent.gamete1,
                    parent.gamete2, pop.gametes, pop.mutations,
                    gamete_recycling_bin, neutral, selected);
                return std::make_pair(offspring_gamete,
                                      std::move(gamete_data));
            }

            template <typename genetic_param_holder,
                      typename mutation_handling_policy, typename poptype>
            inline std::pair<mut_rec_intermediates, mut_rec_intermediates>
            generate_offspring_details(
                fwdpp::poptypes::SINGLELOC_TAG, const gsl_rng* r,
                const std::pair<std::size_t, std::size_t> parents,
                const mutation_handling_policy& mutation_policy, poptype& pop,
                genetic_param_holder& genetics,
                typename poptype::diploid_t& offspring)
            {
                static_assert(
                    std::is_same<typename std::remove_const<decltype(
                                     genetics.interlocus_recombination)>::type,
                                 std::nullptr_t>::value,
                    "invalid genetics policies detected");
                auto p1g1 = pop.diploids[parents.first].first;
                auto p1g2 = pop.diploids[parents.first].second;
                auto p2g1 = pop.diploids[parents.second].first;
                auto p2g2 = pop.diploids[parents.second].second;

                int swap1 = genetics.gamete_swapper(r, p1g1, p1g2);
                int swap2 = genetics.gamete_swapper(r, p2g1, p2g2);

                if (swap1)
                    {
                        std::swap(p1g1, p1g2);
                    }
                if (swap2)
                    {
                        std::swap(p2g1, p2g2);
                    }
                auto offspring_first_gamete_data = generate_offspring_gamete(
                    parental_data{ parents.first, p1g1, p1g2, swap1 },
                    genetics.generate_breakpoints, genetics.generate_mutations,
                    mutation_policy, genetics.mutation_recycling_bin,
                    genetics.gamete_recycling_bin, genetics.neutral,
                    genetics.selected, pop);
                auto offspring_second_gamete_data = generate_offspring_gamete(
                    parental_data{ parents.second, p2g1, p2g2, swap2 },
                    genetics.generate_breakpoints, genetics.generate_mutations,
                    mutation_policy, genetics.mutation_recycling_bin,
                    genetics.gamete_recycling_bin, genetics.neutral,
                    genetics.selected, pop);
                // Update the offspring's gametes.
                offspring.first = offspring_first_gamete_data.first;
                offspring.second = offspring_second_gamete_data.first;
                pop.gametes[offspring.first].n++;
                pop.gametes[offspring.second].n++;
                return std::make_pair(
                    std::move(offspring_first_gamete_data.second),
                    std::move(offspring_second_gamete_data.second));
            }

            inline int
            multilocus_update(const mut_rec_intermediates& gamete_data,
                              std::vector<double>& breakpoints,
                              std::vector<uint_t>& mutation_keys)
            {
                mutation_keys.insert(end(mutation_keys),
                                     begin(gamete_data.mutation_keys),
                                     end(gamete_data.mutation_keys));
                if (gamete_data.breakpoints.empty())
                    {
                        return 0;
                    }
#ifndef NDEBUG
                if (gamete_data.breakpoints.back()
                    != std::numeric_limits<double>::max())
                    {
                        throw std::runtime_error(
                            "FWDPP DEBUG: breakpoints vector missing sentinel "
                            "value");
                    }
#endif
                breakpoints.insert(end(breakpoints),
                                   begin(gamete_data.breakpoints),
                                   end(gamete_data.breakpoints) - 1);
                return gamete_data.breakpoints.size() - 1;
            }

            template <typename genetic_param_holder,
                      typename mutation_handling_policy, typename poptype>
            inline std::pair<mut_rec_intermediates, mut_rec_intermediates>
            generate_offspring_details(
                fwdpp::poptypes::MULTILOC_TAG, const gsl_rng* r,
                const std::pair<std::size_t, std::size_t> parents,
                const mutation_handling_policy& mutation_policy, poptype& pop,
                genetic_param_holder& genetics,
                typename poptype::diploid_t& offspring)
            {
                //TODO need a debugging block on container sizes.
                int swap1 = genetics.gamete_swapper(
                    r, pop.diploids[parents.first][0].first,
                    pop.diploids[parents.first][0].second);
                int swap2 = genetics.gamete_swapper(
                    r, pop.diploids[parents.second][0].first,
                    pop.diploids[parents.second][0].second);
                // NOTE: this logic differs from fwdpp_internal::multilocus_mut_rec
                int ttl_swaps_1 = 0;
                int ttl_swaps_2 = 0;

                decltype(mut_rec_intermediates::breakpoints) all_breakpoints_1,
                    all_breakpoints_2;
                decltype(mut_rec_intermediates::mutation_keys) all_mut_keys_1,
                    all_mut_keys_2;

                const auto& irec = genetics.interlocus_recombination;
                offspring.resize(pop.locus_boundaries.size());
                for (std::size_t i = 0; i < offspring.size(); ++i)
                    {
                        if (i > 0)
                            {
                                // between-locus rec, parent 1
                                auto nrec_bw = irec[i - 1]();
                                if (nrec_bw > 0 && nrec_bw % 2 != 0.)
                                    {
                                        all_breakpoints_1.push_back(
                                            pop.locus_boundaries[i - 1]
                                                .second);
                                    }
                                ttl_swaps_1 += nrec_bw;
                                // between-locus rec, parent 2
                                nrec_bw = irec[i - 1]();
                                ttl_swaps_2 += nrec_bw;
                                if (nrec_bw > 0 && nrec_bw % 2 != 0.)
                                    {
                                        all_breakpoints_2.push_back(
                                            pop.locus_boundaries[i - 1]
                                                .second);
                                    }
                            }
                        auto p1g1 = pop.diploids[parents.first][i].first;
                        auto p1g2 = pop.diploids[parents.first][i].second;
                        auto p2g1 = pop.diploids[parents.second][i].first;
                        auto p2g2 = pop.diploids[parents.second][i].second;
                        // NOTE: this logic differs from fwdpp_internal::multilocus_mut_rec
                        if (swap1)
                            {
                                std::swap(p1g1, p1g2);
                            }
                        if (swap2)
                            {
                                std::swap(p2g1, p2g2);
                            }
                        if (ttl_swaps_1 % 2 != 0.)
                            {
                                std::swap(p1g1, p1g2);
                            }
                        if (ttl_swaps_2 % 2 != 0.)
                            {
                                std::swap(p2g1, p2g2);
                            }
                        auto gamete_data = generate_offspring_gamete(
                            parental_data{ parents.first, p1g1, p1g2, swap1 },
                            genetics.generate_breakpoints[i],
                            genetics.generate_mutations[i], mutation_policy,
                            genetics.mutation_recycling_bin,
                            genetics.gamete_recycling_bin, genetics.neutral,
                            genetics.selected, pop);
                        offspring[i].first = gamete_data.first;
                        debug::gamete_is_sorted(
                            pop.gametes[offspring[i].first], pop.mutations);
                        pop.gametes[gamete_data.first].n++;
                        ttl_swaps_1 += multilocus_update(gamete_data.second,
                                                         all_breakpoints_1,
                                                         all_mut_keys_1);
                        gamete_data = generate_offspring_gamete(
                            parental_data{ parents.second, p2g1, p2g2, swap2 },
                            genetics.generate_breakpoints[i],
                            genetics.generate_mutations[i], mutation_policy,
                            genetics.mutation_recycling_bin,
                            genetics.gamete_recycling_bin, genetics.neutral,
                            genetics.selected, pop);
                        offspring[i].second = gamete_data.first;
                        debug::gamete_is_sorted(
                            pop.gametes[offspring[i].second], pop.mutations);
                        pop.gametes[gamete_data.first].n++;
                        ttl_swaps_2 += multilocus_update(gamete_data.second,
                                                         all_breakpoints_2,
                                                         all_mut_keys_2);
                    }

                if (!all_breakpoints_1.empty())
                    {
                        all_breakpoints_1.push_back(
                            std::numeric_limits<double>::max());
                    }
                if (!all_breakpoints_2.empty())
                    {
                        all_breakpoints_2.push_back(
                            std::numeric_limits<double>::max());
                    }
                return std::make_pair(
                    mut_rec_intermediates(swap1, std::move(all_breakpoints_1),
                                          std::move(all_mut_keys_1)),
                    mut_rec_intermediates(swap2, std::move(all_breakpoints_2),
                                          std::move(all_mut_keys_2)));
            }
        } // namespace detail

        template <typename genetic_param_holder,
                  typename mutation_handling_policy, typename poptype>
        std::pair<mut_rec_intermediates, mut_rec_intermediates>
        generate_offspring(const gsl_rng* r,
                           const std::pair<std::size_t, std::size_t> parents,
                           const mutation_handling_policy& mutation_policy,
                           poptype& pop, genetic_param_holder& genetics,
                           typename poptype::diploid_t& offspring)
        /// \brief Generate offspring gametes and return breakpoints plus mutation keys
        ///
        /// \param r Random number generator
        /// \param parents Indexes of the offspring parents in \a pop
        /// \param mutation_policy Either all_mutations or selected_variants_only.  See below.
        /// \param pop Either fwdpp::poptypes::slocuspop or fwdpp::poptypes::mlocuspop.
        /// \param genetics A duck type of fwdpp::genetic_parameters.
        /// \param offspring The offspring for which we will generate gametes.
        ///
        /// The final three parameters will be modified.
        ///
        /// \return A pair of mut_rec_intermediates, corresponding to what is passed on from
        /// each parent.
        ///
        /// The operations are dispatched out to functions based on the population type.  These
        /// functions make calls to fwdpp::mutate_recombine.
        ///
        /// The parameter \a mutation_policy governs what types of mutations are entered
        /// into the gametes of \a offspring.  If the policy is fwdpp::ts::all_mutations, then
        /// neutral and selected variants are placed in an offspring's gametes.  If the policy is
        /// fwdpp::ts::selected_variants_only, then only selected mutations are placed into the gametes.
        /// Regardless of the policy, ALL mutations are contained in the return value, with the idea
        /// that the caller will record them into a fwdpp::ts::table_collection.
        ///
        /// \note The function type genetic_param_holder::generate_mutations must return
        /// std::vector<fwdpp::uint_t>, with the values reflecting the locations of new
        /// mutations on \a pop.mutations.  Further, this function must already bind
        /// any relevant mutation rates (as this generate_offspring does not accept them
        /// as arguments).
        ///
        /// \version 0.7.4 Added to fwdpp::ts.
        ///
        {
            return detail::generate_offspring_details(
                typename poptype::popmodel_t(), r, parents, mutation_policy,
                pop, genetics, offspring);
        }
    } // namespace ts
} // namespace fwdpp

#endif
